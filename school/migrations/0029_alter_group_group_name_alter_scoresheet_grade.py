# Generated by Django 5.1 on 2025-01-17 20:39

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_applicant_gender_alter_group_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128),
        ),
        migrations.AlterField(
            model_name='scoresheet',
            name='grade',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
    ]
