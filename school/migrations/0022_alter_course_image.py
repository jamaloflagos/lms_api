# Generated by Django 5.1 on 2024-09-09 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0021_remove_course_picture_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/'),
        ),
    ]