from .models import Course
from graphene import Field, List, ObjectType, String
from graphene_django import DjangoObjectType


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class Query(ObjectType):
    courses = List(CourseType)
    course = Field(CourseType, id=String(required=True))

    def resolve_courses(root, info):
        return Course.objects.all()

    def resolve_course(root, info, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            return None


