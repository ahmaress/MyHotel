# Generated by Django 4.1.10 on 2023-12-02 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0005_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_id',
            new_name='id',
        ),
    ]