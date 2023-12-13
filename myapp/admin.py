from django.contrib import admin
from .models import Status, Profile

# Register your models here.

class ModelStatus(admin.ModelAdmin):
    list_display=['timee', 'status']

admin.site.register(Profile)
admin.site.register(Status)

