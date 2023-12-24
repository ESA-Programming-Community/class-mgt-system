# Generated by Django 5.0 on 2023-12-15 11:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0019_alter_studentquizmark_final_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_title', models.CharField(max_length=250)),
                ('assignment_instruction', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(db_default=models.Value(False))),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('community_it_belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgt_app.community')),
                ('module_it_belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mgt_app.module')),
                ('user_posted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]