# Generated by Django 5.1 on 2024-09-05 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_lesson_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30)),
                ('due_date', models.DateField()),
                ('due_time', models.TimeField()),
                ('obtainable_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('topic', models.CharField(max_length=64)),
                ('tutor', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('picture', models.FilePathField()),
                ('creator', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('day', models.CharField(max_length=10)),
                ('obtainable_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('estimated_time', models.SmallIntegerField(default=None, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='has_quiz',
            new_name='has_unit_test',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='content',
            new_name='note',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='topic',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='quiz',
            new_name='unit_test',
        ),
        migrations.RemoveField(
            model_name='class',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='_class',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='score',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='score',
            name='subject',
        ),
        # migrations.AddField(
        #     model_name='lesson',
        #     name='estimated_time',
        #     field=models.SmallIntegerField(default=None),
        # ),
        migrations.AlterField(
            model_name='score',
            name='date_submitted',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='assignment',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='school.lesson'),
        ),
        migrations.AddField(
            model_name='course',
            name='_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='school.class'),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_schedules', to='school.course'),
        ),
        migrations.AddField(
            model_name='exam',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='school.course'),
        ),
        migrations.AddField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='school.course'),
        ),
        # migrations.AddField(
        #     model_name='lesson',
        #     name='module',
        #     field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='school.module'),
        # ),
    ]
