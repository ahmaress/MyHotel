# Generated by Django 4.1.10 on 2023-11-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_status_duty_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='timee',
        ),
        migrations.AlterField(
            model_name='status',
            name='duty_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
