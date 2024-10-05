# Generated by Django 5.1 on 2024-09-02 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=64)),
                ('copies', models.IntegerField()),
                ('location', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('nick_name', models.CharField(max_length=24)),
                ('category', models.CharField(max_length=24)),
                ('subjects', models.JSONField(blank=True, default=list)),
            ],
            options={
                'db_table': 'class',
            },
        ),
        migrations.CreateModel(
            name='EntranceExamQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('options', models.JSONField(default=list)),
                ('answer', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EntranceExamScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_id', models.CharField(max_length=10, unique=True)),
                ('value', models.SmallIntegerField()),
                ('percentage', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('contact_mail', models.EmailField(default=None, max_length=254)),
                ('address', models.TextField()),
                ('contact_phone', models.CharField(max_length=24)),
                ('emergency_phone', models.CharField(max_length=24)),
            ],
            options={
                'db_table': 'parent',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BookPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchased', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('supplier', models.CharField(max_length=30)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='school.book')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_id', models.CharField(max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('contact_mail', models.EmailField(default=None, max_length=254, unique=True)),
                ('address', models.TextField()),
                ('contact_phone', models.CharField(max_length=24)),
                ('parent_first_name', models.CharField(max_length=64)),
                ('parent_last_name', models.CharField(max_length=64)),
                ('parent_contact_mail', models.EmailField(default=None, max_length=254)),
                ('parent_address', models.TextField()),
                ('parent_contact_phone', models.CharField(max_length=24)),
                ('class_applied_for', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='school.class')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=64)),
                ('topic', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('has_quiz', models.BooleanField(default=False)),
                ('quiz', models.JSONField(blank=True, default=list)),
                ('has_video', models.BooleanField(default=False)),
                ('video', models.TextField()),
                ('date_created', models.DateField()),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='school.class')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(default=None, max_length=254, unique=True)),
                ('password', models.CharField(default=None, max_length=64)),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.class')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='school.parent')),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=64)),
                ('value', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_checked_out', models.DateTimeField()),
                ('days_requested', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to='school.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_borrowed', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='BookSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sold', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='school.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('subjects', models.JSONField(blank=True, default=list)),
                ('is_form_teacher', models.BooleanField(default=False)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('password', models.CharField(default=None, max_length=64, null=True)),
                ('_class', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='form_teacher', to='school.class')),
            ],
            options={
                'db_table': 'teacher',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=68)),
                ('type', models.CharField(max_length=10)),
                ('value', models.IntegerField()),
                ('date_submitted', models.DateTimeField()),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='school.lesson')),
                ('student', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='school.student')),
            ],
            options={
                'unique_together': {('student', 'lesson', 'type')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_marked', models.DateTimeField()),
                ('status', models.CharField(max_length=7)),
                ('_class', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='school.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='school.student')),
            ],
            options={
                'unique_together': {('student', 'date_marked')},
            },
        ),
    ]