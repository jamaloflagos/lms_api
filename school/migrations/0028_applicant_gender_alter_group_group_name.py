# Generated by Django 5.1 on 2025-01-17 20:23

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0027_remove_student_student_id_alter_group_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default=None, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128),
        ),
    ]
