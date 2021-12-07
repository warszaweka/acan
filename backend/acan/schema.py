from base64 import b64encode
from decimal import Decimal
from hashlib import sha1
from json import dumps
from smtplib import SMTPRecipientsRefused

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import DataError, IntegrityError
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import activate, get_language
from graphene import Boolean, Field, List, NonNull, ObjectType, String
from graphene_django import DjangoObjectType

from .models import Course, Lesson, Order, User, UserManager
from .tokens import email_verify_token, password_reset_token


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = ('id', 'soon', 'title', 'image', 'short_description',
                  'description', 'cost', 'lesson_set')

    purchased = Boolean(required=True)

    def resolve_purchased(parent, info):
        return parent.purchased(info.context.user)

    def resolve_description(parent, info):
        if parent.published:
            return parent.description
        return ""

    def resolve_cost(parent, info):
        if parent.published:
            return parent.cost
        return Decimal(0)

    def resolve_lesson_set(parent, info):
        if parent.published:
            return parent.lesson_set.all()
        return Lesson.objects.none()


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'order', 'title', 'description', 'video',
                  'addon')

    def resolve_description(parent, info):
        if parent.course.purchased(info.context.user):
            return parent.description
        return ""

    def resolve_video(parent, info):
        if parent.course.purchased(info.context.user):
            return parent.video
        return ""

    def resolve_addon(parent, info):
        if parent.course.purchased(info.context.user):
            return parent.addon


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'mailing_list')


class Query(ObjectType):
    courses = List(NonNull(CourseType), required=True)
    course = Field(CourseType, id=String(required=True))
    lesson = Field(LessonType, id=String(required=True))
    user = Field(UserType)
    language = String(required=True)

    def resolve_courses(root, info):
        return Course.objects.filter(Q(published=True) | Q(soon=True)).all()

    def resolve_course(root, info, id):
        try:
            return Course.objects.get(Q(published=True) | Q(soon=True), pk=id)
        except Course.DoesNotExist:
            pass

    def resolve_lesson(root, info, id):
        try:
            return Lesson.objects.get(pk=id, course__published=True)
        except Lesson.DoesNotExist:
            pass

    def resolve_user(root, info):
        user = info.context.user
        if user.is_authenticated:
            return user

    def resolve_language(root, info):
        return get_language()


class CreateOrderResult(ObjectType):
    data = String(required=True)
    signature = String(required=True)

    def resolve_data(parent, info):
        return parent['data']

    def resolve_signature(parent, info):
        return parent['signature']


class Mutation(ObjectType):
    login = Field(String,
                  email=String(required=True),
                  password=String(required=True))
    logout = Boolean(required=True)
    signup = Field(String,
                   email=String(required=True),
                   password=String(required=True),
                   phone=String(required=True),
                   first_name=String(required=True),
                   last_name=String(required=True),
                   mailing_list=Boolean())
    email_verify = Field(Boolean,
                         required=True,
                         uidb64=String(required=True),
                         token=String(required=True))
    set_password = Field(Boolean,
                         required=True,
                         password=String(required=True))
    set_mailing_list = Field(Boolean,
                             required=True,
                             mailing_list=Boolean(required=True))
    request_password_reset = Field(String, email=String(required=True))
    password_reset = Field(Boolean,
                           required=True,
                           uidb64=String(required=True),
                           token=String(required=True),
                           password=String(required=True))
    create_order = Field(CreateOrderResult, id=String(required=True))
    set_language = Field(Boolean,
                         required=True,
                         language=String(required=True))

    def resolve_login(root, info, email, password):
        context = info.context
        email = UserManager.normalize_email(email)
        user = authenticate(context, username=email, password=password)
        if not user:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                if not user.is_active:
                    return 'Unverified email'
            return 'Invalid credentials'
        login(context, user)

    def resolve_logout(root, info):
        logout(info.context)
        return True

    def resolve_signup(root,
                       info,
                       email,
                       password,
                       phone,
                       first_name,
                       last_name,
                       mailing_list=None):
        try:
            user = User.objects.create_user(email=email,
                                            password=password,
                                            phone=phone,
                                            first_name=first_name,
                                            last_name=last_name)
            if mailing_list:
                user.mailing_list = mailing_list
                user.save()
        except IntegrityError:
            return 'Used email'
        except DataError:
            return 'Unvalid values'
        else:
            try:
                send_mail(
                    'Email verify',
                    render_to_string(
                        'acan/email_verify.html', {
                            'url': settings.ACAN_EMAIL_VERIFY_URL,
                            'uidb64': urlsafe_base64_encode(
                                force_bytes(user.pk)),
                            'token': email_verify_token.make_token(user),
                        }),
                    settings.ACAN_EMAIL_FROM,
                    [user.email],
                )
            except SMTPRecipientsRefused:
                user.delete()
                return 'Unvalid email'

    def resolve_email_verify(root, info, uidb64, token):
        try:
            user = User.objects.get(
                pk=force_text(urlsafe_base64_decode(uidb64)))
            if email_verify_token.check_token(user, token):
                user.is_active = True
                user.save()
        except Exception:
            pass
        return True

    def resolve_set_password(root, info, password):
        user = info.context.user
        if user.is_authenticated:
            user.set_password(password)
            user.save()
        return True

    def resolve_set_mailing_list(root, info, mailing_list):
        user = info.context.user
        if user.is_authenticated:
            user.mailing_list = mailing_list
            user.save()
        return True

    def resolve_request_password_reset(root, info, email):
        email = UserManager.normalize_email(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return 'Unused email'
        else:
            send_mail(
                'Password reset',
                render_to_string(
                    'acan/password_reset.html', {
                        'url': settings.ACAN_PASSWORD_RESET_URL,
                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': password_reset_token.make_token(user),
                    }),
                settings.ACAN_EMAIL_FROM,
                [email],
            )

    def resolve_password_reset(root, info, uidb64, token, password):
        try:
            user = User.objects.get(
                pk=force_text(urlsafe_base64_decode(uidb64)))
            if password_reset_token.check_token(user, token):
                user.set_password(password)
                user.save()
        except Exception:
            pass
        return True

    def resolve_create_order(root, info, id):
        user = info.context.user
        if user.is_authenticated:
            try:
                course = Course.objects.get(pk=id, published=True)
            except Course.DoesNotExist:
                pass
            else:
                order = Order.objects.create(user_id=user.id, course_id=id)
                data = b64encode(
                    dumps({
                        'version':
                        '3',
                        'public_key':
                        settings.LIQPAY_PUBLIC_KEY,
                        'action':
                        'pay',
                        'amount':
                        str(course.cost),
                        'currency':
                        'UAH',
                        'description':
                        str(course.title),
                        'order_id':
                        str(order.id),
                        'server_url':
                        info.context.build_absolute_uri(
                            reverse('acan:payment')),
                    }).encode('utf-8')).decode('ascii')
                return {
                    'data':
                    data,
                    'signature':
                    b64encode(
                        sha1(
                            f'{settings.LIQPAY_PRIVATE_KEY}{data}{settings.LIQPAY_PRIVATE_KEY}'
                            .encode('utf-8')).digest()).decode('ascii'),
                }

    def resolve_set_language(root, info, language):
        if language in [
                language_tuple[0] for language_tuple in settings.LANGUAGES
        ]:
            activate(language)
            info.context.acan_set_language_cookie = language
        return True
