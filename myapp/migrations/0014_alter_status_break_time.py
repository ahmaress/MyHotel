# Generated by Django 4.1.10 on 2023-11-28 14:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_status_break_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='break_time',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]