# Generated by Django 5.0 on 2023-12-05 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0012_rename_question_question_question_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentQuizMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_score', models.CharField(max_length=200)),
                ('attempted', models.BooleanField()),
                ('date_completed', models.DateTimeField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]