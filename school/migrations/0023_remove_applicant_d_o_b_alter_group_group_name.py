# Generated by Django 5.1 on 2025-01-17 09:59

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_rename_email_applicant_contact_mail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='d_o_b',
        ),
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128),
        ),
    ]
