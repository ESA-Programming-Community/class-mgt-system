# Generated by Django 5.0 on 2023-12-15 15:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0021_assignment_assignment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='mode_of_submission',
            field=models.CharField(choices=[('In person', 'In person'), ('Online', 'Online')], db_default=models.Value('Online'), max_length=300),
        ),
        migrations.AddField(
            model_name='assignment',
            name='preferred_submission_format',
            field=models.CharField(db_default=models.Value('URL Submission'), max_length=200),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('file_submission', models.FileField(blank=True, null=True, upload_to='files/')),
                ('text_submission', models.TextField(blank=True, null=True)),
                ('url_submission', models.URLField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
