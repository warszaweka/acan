# Generated by Django 3.2.13 on 2022-05-15 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acan', '0006_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='article_images/'),
        ),
    ]
