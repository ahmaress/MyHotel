# Generated by Django 4.1.10 on 2023-11-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_timestamp_status_timee'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]