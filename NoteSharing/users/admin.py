from django.contrib import admin
from .models import UserTag,Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(UserTag)