# Generated by Django 5.0 on 2023-12-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgt_app', '0020_assignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='assignment_number',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
