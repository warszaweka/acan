from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import activate, get_language
from django.utils.translation import gettext as _
from graphene import Boolean, Field, List, NonNull, ObjectType, String
from graphene_django import DjangoObjectType
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Course, Lesson, Order, User, UserManager
from .tokens import email_verify_token, password_reset_token


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = ('id', 'title', 'short_description', 'description', 'cost'
                  'lesson_set')

    purchased = Field(Boolean, required=True)

    def resolve_purchased(parent, info):
        return parent.purchased(info.context.user)


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

    def resolve_file(parent, info):
        if parent.course.purchased(info.context.user):
            return parent.file
        return None


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('email', )

    courses = List(NonNull(CourseType), required=True)

    def resolve_courses(parent, info):
        return parent.courses()


class Query(ObjectType):
    courses = List(NonNull(CourseType), required=True)
    course = Field(CourseType, id=String(required=True))
    lesson = Field(LessonType, id=String(required=True))
    user = Field(UserType)
    language = Field(NonNull(String))

    def resolve_courses(*args, **kwargs):
        return Course.objects.all()

    def resolve_course(root, info, id):
        try:
            return Course.objects.get(pk=id)
        except Course.DoesNotExist:
            return None

    def resolve_lesson(root, info, id):
        try:
            return Lesson.objects.get(pk=id)
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
    success = Field(NonNull(Boolean))
    user = Field(UserType)
    error = Field(String)

    def resolve_success(parent, info):
        return parent['success']

    def resolve_user(parent, info):
        if 'user' in parent:
            return parent['user']
        return None

    def resolve_error(parent, *args, **kwargs):
        if 'error' in parent:
            return parent['error']
        return None


class LogoutResult(ObjectType):
    user = Field(UserType)
    courses = List(NonNull(CourseType))

    def resolve_user(parent, info):
        return parent['user']

    def resolve_courses(parent, *args, **kwargs):
        return parent['courses']


class SetLanguageResult(ObjectType):
    success = Field(NonNull(Boolean))
    language = Field(String)
    courses = List(NonNull(CourseType))

    def resolve_success(parent, info):
        return parent['success']

    def resolve_language(parent, info):
        if 'language' in parent:
            return parent['language']
        return None

    def resolve_courses(parent, info):
        if 'courses' in parent:
            return parent['courses']
        return None


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
    create_order = Field(String, id=String(required=True))
    set_language = Field(NonNull(SetLanguageResult),
                         language=String(required=True))

    def resolve_login(root, info, email, password):
        error = None
        context = info.context
        if not context.user.is_authenticated:
            email = UserManager.normalize_email(email)
            user = User.objects.get(email=email)
            if not user.is_active:
                error = 'Unverified email'
            else:
                user = authenticate(context, username=email, password=password)
                if not user:
                    error = 'Invalid credentials'
                else:
                    login(context, user)
                    return {
                        'success': True,
                        'user': user,
                    }
        return {
            'success': False,
            'error': error,
        }

    def resolve_logout(root, info):
        logout(info.context)
        return {
            'user': None,
            'courses': Course.objects.all(),
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
                return Order.objects.create(user_id=user.id, course_id=id).pk
            except Exception:
                pass
        return None

    def resolve_set_language(root, info, language):
        if language in [
                language_tuple[0] for language_tuple in settings.LANGUAGES
        ]:
            activate(language)
            info.context.acan_set_language_cookie = language
            return {
                'success': True,
                'language': laguage,
                'courses': Course.objects.all(),
            }
        return {
            'success': False,
        }
