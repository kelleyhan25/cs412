# File: mini_fb/admin.py 
# Author: Kelley Han kelhan@bu.edu 
# Description: Registers the Profile model to admin 


from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile)
admin.site.register(StatusMessage)