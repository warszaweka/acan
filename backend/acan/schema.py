from base64 import b64encode
from decimal import Decimal
from hashlib import sha1
from json import dumps

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import activate, get_language
from graphene import Boolean, Field, List, NonNull, ObjectType, String
from graphene_django import DjangoObjectType
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Course, Lesson, Order, User, UserManager
from .tokens import email_verify_token, password_reset_token


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = ('id', 'soon', 'title', 'image', 'short_description',
                  'description', 'cost', 'lesson_set')

    purchased = Field(Boolean, required=True)

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
        return None


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('email', )


class Query(ObjectType):
    courses = List(NonNull(CourseType), required=True)
    course = Field(CourseType, id=String(required=True))
    lesson = Field(LessonType, id=String(required=True))
    user = Field(UserType)
    language = Field(NonNull(String))

    def resolve_courses(*args, **kwargs):
        return Course.objects.filter(Q(published=True) | Q(soon=True)).all()

    def resolve_course(root, info, id):
        try:
            return Course.objects.get(Q(published=True) | Q(soon=True), pk=id)
        except Course.DoesNotExist:
            return None

    def resolve_lesson(root, info, id):
        try:
            return Lesson.objects.get(pk=id, course__published=True)
        except Lesson.DoesNotExist:
            return None

    def resolve_user(root, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    def resolve_language(*args, **kwargs):
        return get_language()


class LoginResult(ObjectType):
    user = Field(UserType)
    courses = List(NonNull(CourseType))
    error = Field(String)

    def resolve_user(parent, *args, **kwargs):
        return parent['user']

    def resolve_courses(parent, *args, **kwargs):
        return parent['courses']

    def resolve_error(parent, *args, **kwargs):
        return parent['error']


class LogoutResult(ObjectType):
    user = Field(UserType)
    courses = List(NonNull(CourseType), required=True)

    def resolve_user(parent, *args, **kwargs):
        return parent['user']

    def resolve_courses(parent, *args, **kwargs):
        return parent['courses']


class SetLanguageResult(ObjectType):
    language = Field(String)
    courses = List(NonNull(CourseType))

    def resolve_language(parent, info):
        return parent['language']

    def resolve_courses(parent, info):
        return parent['courses']


class CreateOrderResult(ObjectType):
    data = Field(String)
    signature = Field(String)

    def resolve_data(parent, info):
        return parent['data']

    def resolve_signature(parent, info):
        return parent['signature']


class Mutation(ObjectType):
    login = Field(NonNull(LoginResult),
                  email=String(required=True),
                  password=String(required=True))
    logout = NonNull(LogoutResult)
    signup = Field(String,
                   email=String(required=True),
                   password=String(required=True))
    email_verify = Field(NonNull(Boolean),
                         uidb64=String(required=True),
                         token=String(required=True))
    set_password = Field(NonNull(Boolean), password=String(required=True))
    request_password_reset = Field(String, email=String(required=True))
    password_reset = Field(Boolean,
                           uidb64=String(required=True),
                           token=String(required=True),
                           password=String(required=True))
    create_order = Field(NonNull(CreateOrderResult), id=String(required=True))
    set_language = Field(NonNull(SetLanguageResult),
                         language=String(required=True))

    def resolve_login(root, info, email, password):
        error = None
        context = info.context
        if not context.user.is_authenticated:
            email = UserManager.normalize_email(email)
            user = authenticate(context, username=email, password=password)
            if not user:
                error = 'Invalid credentials'
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    pass
                else:
                    if not user.is_active:
                        error = 'Unverified email'
            else:
                login(context, user)
                return {
                    'user':
                    user,
                    'courses':
                    Course.objects.filter(Q(published=True)
                                          | Q(soon=True)).all(),
                    'error':
                    error,
                }
        return {
            'user': None,
            'courses': None,
            'error': error,
        }

    def resolve_logout(root, info):
        logout(info.context)
        return {
            'user':
            None,
            'courses':
            Course.objects.filter(Q(published=True) | Q(soon=True)).all(),
        }

    def resolve_signup(root, info, email, password):
        try:
            user = User.objects.create_user(email=email, password=password)
        except IntegrityError:
            return 'Used email'
        else:
            try:
                SendGridAPIClient(settings.ACAN_SENDGRID_API_KEY).send(
                    Mail(from_email=settings.ACAN_EMAIL_FROM,
                         to_emails=user.email,
                         subject='Email verify',
                         html_content=render_to_string(
                             'acan/email_verify.html', {
                                 'url':
                                 settings.ACAN_EMAIL_VERIFY_URL,
                                 'uidb64':
                                 urlsafe_base64_encode(force_bytes(user.pk)),
                                 'token':
                                 email_verify_token.make_token(user),
                             })))
                return None
            except Exception:
                return 'Unvalid email'

    def resolve_email_verify(root, info, uidb64, token):
        try:
            user = User.objects.get(
                pk=force_text(urlsafe_base64_decode(uidb64)))
            if email_verify_token.check_token(user, token):
                user.is_active = True
                user.save()
                return True
        except Exception:
            pass
        return False

    def resolve_set_password(root, info, password):
        user = info.context.user
        if user.is_authenticated:
            user.set_password(password)
            user.save()
            return True
        return False

    def resolve_request_password_reset(root, info, email):
        email = UserManager.normalize_email(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return 'Unused email'
        else:
            SendGridAPIClient(settings.ACAN_SENDGRID_API_KEY).send(
                Mail(from_email=settings.ACAN_EMAIL_FROM,
                     to_emails=email,
                     subject='Password reset',
                     html_content=render_to_string(
                         'acan/password_reset.html', {
                             'url': settings.ACAN_PASSWORD_RESET_URL,
                             'uidb64': urlsafe_base64_encode(
                                 force_bytes(user.pk)),
                             'token': password_reset_token.make_token(user),
                         })))
            return None

    def resolve_password_reset(root, info, uidb64, token, password):
        try:
            user = User.objects.get(
                pk=force_text(urlsafe_base64_decode(uidb64)))
            if password_reset_token.check_token(user, token):
                user.set_password(password)
                user.save()
                return True
        except Exception:
            pass
        return False

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
        return {
            'data': None,
            'signature': None,
        }

    def resolve_set_language(root, info, language):
        if language in [
                language_tuple[0] for language_tuple in settings.LANGUAGES
        ]:
            activate(language)
            info.context.acan_set_language_cookie = language
            return {
                'language':
                language,
                'courses':
                Course.objects.filter(Q(published=True) | Q(soon=True)).all(),
            }
        return {
            'language': None,
            'courses': None,
        }
