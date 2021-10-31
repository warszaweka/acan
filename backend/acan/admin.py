from django.contrib.admin import ModelAdmin, register

from .models import Course, Lesson, Profile


@register(Course)
class CourseAdmin(ModelAdmin):
    pass


@register(Lesson)
class LessonAdmin(ModelAdmin):
    pass


@register(Profile)
class ProfileAdmin(ModelAdmin):
    pass
