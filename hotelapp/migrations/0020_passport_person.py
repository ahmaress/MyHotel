# Generated by Django 4.1.10 on 2023-12-18 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0019_category_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(max_length=20, unique=True)),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('country_of_issue', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('passport', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotelapp.passport')),
            ],
        ),
    ]