# Generated by Django 4.1.10 on 2023-12-07 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0009_room_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='room_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]