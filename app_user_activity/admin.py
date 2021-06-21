from django.contrib import admin
from app_user_activity import models

# Register your models here.

admin.site.register(models.UserPost)
admin.site.register(models.Like)
admin.site.register(models.Follow)
