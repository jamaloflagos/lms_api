# Generated by Django 5.1 on 2024-09-06 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_alter_lesson_estimated_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='school.module', null=True),
        ),
    ]