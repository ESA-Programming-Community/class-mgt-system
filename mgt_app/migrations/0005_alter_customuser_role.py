# Generated by Django 4.2.4 on 2023-11-14 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0004_alter_community_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('Student', 'Student'), ('Instructor', 'Instructor'), ('Co-Instructor', 'Co-Instructor'), ('Admin', 'Admin')], default='Student', max_length=200, null=True),
        ),
    ]