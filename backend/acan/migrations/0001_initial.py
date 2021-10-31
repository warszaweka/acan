from django.conf import settings
from django.db.migrations import CreateModel
from django.db.migrations import Migration as MigrationsMigration
from django.db.migrations import swappable_dependency
from django.db.models import (BigAutoField, CharField, FileField, ForeignKey,
                              ManyToManyField, OneToOneField,
                              PositiveSmallIntegerField, TextField)
from django.db.models.deletion import CASCADE


class Migration(MigrationsMigration):
    initial = True
    dependencies = [
        swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        CreateModel(name='Course',
                    fields=[
                        ('id',
                         BigAutoField(auto_created=True,
                                      primary_key=True,
                                      serialize=False,
                                      verbose_name='ID')),
                        ('title', CharField(max_length=128)),
                        ('description', TextField()),
                    ]),
        CreateModel(name='Profile',
                    fields=[
                        ('id',
                         BigAutoField(auto_created=True,
                                      primary_key=True,
                                      serialize=False,
                                      verbose_name='ID')),
                        ('courses', ManyToManyField(to='acan.Course')),
                        ('user',
                         OneToOneField(on_delete=CASCADE,
                                       to=settings.AUTH_USER_MODEL)),
                    ]),
        CreateModel(name='Lesson',
                    fields=[
                        ('id',
                         BigAutoField(auto_created=True,
                                      primary_key=True,
                                      serialize=False,
                                      verbose_name='ID')),
                        ('order', PositiveSmallIntegerField()),
                        ('title', CharField(max_length=128)),
                        ('description', TextField()),
                        ('video', FileField(upload_to='')),
                        ('addon', FileField(blank=True,
                                            null=True,
                                            upload_to='')),
                        ('course',
                         ForeignKey(on_delete=CASCADE, to='acan.course')),
                    ]),
    ]
