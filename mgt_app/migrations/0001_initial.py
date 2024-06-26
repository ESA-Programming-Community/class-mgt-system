# Generated by Django 5.0 on 2024-06-07 21:31

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('faculty_head', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveIntegerField()),
                ('question_text', models.TextField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('approved', models.BooleanField(default=False)),
                ('role', models.CharField(blank=True, choices=[('Student', 'Student'), ('Instructor', 'Instructor'), ('Co-Instructor', 'Co-Instructor'), ('Admin', 'Admin')], default='Student', max_length=200, null=True)),
                ('phone_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('password1', models.CharField(max_length=100)),
                ('password2', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('requirements', models.TextField(blank=True, max_length=500, null=True)),
                ('group_link', models.URLField(blank=True, null=True)),
                ('co_instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assistant_instructor', to=settings.AUTH_USER_MODEL)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_instructor', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_number', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('community_it_belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.community')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=400, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('module_it_belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mgt_app.module')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_number', models.PositiveBigIntegerField()),
                ('assignment_title', models.CharField(max_length=250)),
                ('assignment_instruction', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('mode_of_submission', models.CharField(choices=[('In person', 'In person'), ('Online', 'Online')], default='Online', max_length=300)),
                ('preferred_submission_format', models.CharField(default='URL Submission', max_length=200)),
                ('user_posted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('community_it_belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.community')),
                ('module_it_belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mgt_app.module')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.faculty')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mgt_app.program'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=256)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.question')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_number', models.PositiveIntegerField(auto_created=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=400, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Dead', 'Dead')], default='Dead', max_length=200)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('community_it_belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.community')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz_it_belongs_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.quiz'),
        ),
        migrations.CreateModel(
            name='RequirementFulfillment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fulfilled', models.BooleanField(default=False)),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mgt_app.community')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=400, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('lesson_it_belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mgt_app.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentQuizMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_score', models.CharField(blank=True, max_length=200, null=True)),
                ('attempted', models.BooleanField()),
                ('date_completed', models.DateTimeField()),
                ('total_score_for_quiz', models.PositiveIntegerField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('file_submission', models.FileField(blank=True, null=True, upload_to='submissions/')),
                ('text_submission', models.TextField(blank=True, null=True)),
                ('url_submission', models.URLField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('student_note', models.TextField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
