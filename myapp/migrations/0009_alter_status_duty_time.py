# Generated by Django 4.1.10 on 2023-11-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_status_timee_alter_status_duty_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='duty_time',
            field=models.DateTimeField(null=True),
        ),
    ]
