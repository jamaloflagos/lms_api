# Generated by Django 5.1 on 2025-01-19 11:44

import django.db.models.deletion
import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0030_student_user_alter_group_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128),
        ),
        migrations.AlterField(
            model_name='outline',
            name='class_subject',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outlines', to='school.classsubject'),
        ),
    ]
