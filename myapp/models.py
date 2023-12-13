# models.py
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    CHECKED_IN = 'checkedin'
    CHECKED_OUT = 'checkedout'
    BREAKED_IN = 'breakedin'
    BREAKED_OUT = 'breakedout'

    STATUS_CHOICES = [
        (CHECKED_IN, 'Checked In'),
        (CHECKED_OUT, 'Checked Out'),
        (BREAKED_IN, 'Breaked In'),
        (BREAKED_OUT, 'Breaked Out'),
    ]
    

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CHECKED_OUT)
    checkedin_time = models.DateTimeField(null=True)
    breakedin_time = models.DateTimeField(null=True)
    checkedout_time = models.DateTimeField(null=True)
    breakedout_time = models.DateTimeField(null=True)
    duty_time = models.DurationField(null=True)
    break_time = models.DurationField(default=timedelta)
  


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_status = models.ForeignKey(Status, on_delete=models.CASCADE)