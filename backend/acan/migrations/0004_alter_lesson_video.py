# Generated by Django 3.2.9 on 2021-11-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acan', '0003_alter_lesson_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.FileField(default='kek', upload_to=''),
            preserve_default=False,
        ),
    ]
