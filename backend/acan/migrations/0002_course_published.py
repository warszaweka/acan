# Generated by Django 3.2.9 on 2021-11-11 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
