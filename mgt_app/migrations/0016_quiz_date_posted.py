# Generated by Django 5.0 on 2023-12-07 09:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0015_studentquizmark_total_score_for_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]