# Generated by Django 4.1.10 on 2023-12-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0025_alter_userinfo_cnic_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='issue_date',
            field=models.DateField(null=True),
        ),
    ]