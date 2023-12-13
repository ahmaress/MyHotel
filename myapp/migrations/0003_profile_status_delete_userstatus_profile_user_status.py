# Generated by Django 4.1.10 on 2023-11-23 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0002_userstatus_user_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('checkedIn', 'Checked In'), ('checkedOut', 'Checked Out'), ('breakedIn', 'Breaked In'), ('breakedOut', 'Breaked Out')], default='checkedOut', max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='UserStatus',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.status'),
        ),
    ]