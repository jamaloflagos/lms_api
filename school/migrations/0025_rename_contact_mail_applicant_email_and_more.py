# Generated by Django 5.1 on 2025-01-17 10:01

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0024_remove_applicant_has_made_payment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='contact_mail',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='applicant',
            old_name='parent_contact_mail',
            new_name='parent_email',
        ),
        migrations.RenameField(
            model_name='applicant',
            old_name='contact_phone',
            new_name='parent_phone_number',
        ),
        migrations.RenameField(
            model_name='applicant',
            old_name='parent_contact_phone',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='applicant',
            name='d_o_b',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='has_made_payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128),
        ),
    ]
