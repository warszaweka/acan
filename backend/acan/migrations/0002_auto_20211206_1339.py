# Generated by Django 3.2.9 on 2021-12-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
    ]
