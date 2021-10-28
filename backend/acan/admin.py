from django.contrib.admin import ModelAdmin, register

from .models import Course


@register(Course)
class CourseAdmin(ModelAdmin):
    pass
