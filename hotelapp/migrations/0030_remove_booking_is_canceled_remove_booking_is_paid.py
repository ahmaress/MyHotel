# Generated by Django 4.1.10 on 2023-12-28 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0029_booking_is_canceled_booking_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='is_canceled',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='is_paid',
        ),
    ]