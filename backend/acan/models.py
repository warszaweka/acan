from django.contrib.auth import get_user_model
from django.db.models import (CASCADE, CharField, FileField, ForeignKey,
                              ManyToManyField, Model, OneToOneField,
                              PositiveSmallIntegerField, TextField)
from django.db.models.signals import post_save
from django.dispatch import receiver

user_model = get_user_model()


class Course(Model):
    title = CharField(max_length=128)
    description = TextField()

    def purchased(self, user):
        if user.is_authenticated and Course.objects.filter(
                profile__user__id=user.id, id=self.id).exists():
            return True
        return False


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE)
    order = PositiveSmallIntegerField()
    title = CharField(max_length=128)
    description = TextField()
    video = FileField()
    addon = FileField(null=True, blank=True)


class Profile(Model):
    user = OneToOneField(user_model, on_delete=CASCADE)
    courses = ManyToManyField(Course)


@receiver(post_save, sender=user_model)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
