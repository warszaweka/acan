from django.contrib.auth import authenticate, get_user_model, login, logout
from graphene import Boolean, Field, List, NonNull, ObjectType, String
from graphene_django import DjangoObjectType

from .models import Course, Lesson


class CourseType(DjangoObjectType):
    class Meta:
        model = Course

    purchased = Field(Boolean, required=True)

    def resolve_purchased(parent, info):
        return parent.purchased(info.context.user)


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson

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
        model = get_user_model()
        fields = ('username', )


class Query(ObjectType):
    courses = List(NonNull(CourseType), required=True)
    course = Field(CourseType, id=String(required=True))
    lesson = Field(LessonType, id=String(required=True))
    user = Field(UserType)
    login = Field(UserType,
                  username=String(required=True),
                  password=String(required=True))
    logout = Field(Boolean)

    def resolve_courses(root, info):
        return Course.objects.all()

    def resolve_course(root, info, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            return None

    def resolve_lesson(root, info, id):
        try:
            return Lesson.objects.get(id=id)
        except Lesson.DoesNotExist:
            return None

    def resolve_user(root, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    def resolve_login(root, info, username, password):
        context = info.context
        user = authenticate(context, username=username, password=password)
        if user:
            login(context, user)
            return user
        return None

    def resolve_logout(root, info):
        logout(info.context)
        return True
