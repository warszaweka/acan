from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.forms import CharField, ModelForm, PasswordInput
from modeltranslation.admin import TranslationAdmin

from .models import Course, Lesson, Order, User


@register(Course)
class CourseAdmin(TranslationAdmin):
    pass


@register(Lesson)
class LessonAdmin(TranslationAdmin):
    pass


class UserCreationForm(ModelForm):
    password = CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('is_staff', 'is_active')


@register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = ((None, {'fields': ('is_staff', 'is_active')}), )
    add_fieldsets = ((None, {
        'fields': ('email', 'password'),
    }), )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


site.unregister(Group)


@register(Order)
class OrderAdmin(ModelAdmin):
    pass
