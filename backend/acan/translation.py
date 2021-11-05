from modeltranslation.translator import TranslationOptions, register

from .models import Course, Lesson


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'description')
    required_languages = ('uk', 'ru')


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('uk', 'ru')
