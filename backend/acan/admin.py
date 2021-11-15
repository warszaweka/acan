import ffmpeg
from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.files.storage import default_storage
from django.forms import CharField, ModelForm, PasswordInput
from modeltranslation.admin import TranslationAdmin

from .models import Course, Lesson, Order, User


@register(Course)
class CourseAdmin(TranslationAdmin):
    pass


@register(Lesson)
class LessonAdmin(TranslationAdmin):
    def save_model(self, request, obj, *args, **kwargs):
        super().save_model(request, obj, *args, **kwargs)
        old_video = obj.video
        new_video = f'lesson_{obj.id}_.m3u8'
        new_video_path = default_storage.path(new_video)
        ffmpeg.input(old_video.path).output(new_video_path,
                                            acodec='aac',
                                            vcodec='copy',
                                            start_number=0,
                                            hls_time=10,
                                            hls_list_size=0,
                                            f='hls').run()
        old_video.delete(save=False)
        obj.video = new_video
        obj.save()


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
