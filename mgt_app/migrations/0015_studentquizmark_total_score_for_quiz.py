# Generated by Django 5.0 on 2023-12-05 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0014_quiz_quiz_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentquizmark',
            name='total_score_for_quiz',
            field=models.PositiveIntegerField(default=3),
            preserve_default=False,
        ),
    ]
