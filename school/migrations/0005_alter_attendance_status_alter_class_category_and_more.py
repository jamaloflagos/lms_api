# Generated by Django 5.1 on 2025-01-01 09:25

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_studygroup_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(max_length=7),
        ),
        migrations.AlterField(
            model_name='class',
            name='category',
            field=models.CharField(choices=[('Secondary', 'Secondary'), ('Primary', 'Primary')], max_length=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Waitlisted', 'Waitlisted')], default='Open', max_length=10),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student'), ('applicant', 'Applicant')], max_length=10),
        ),
    ]
