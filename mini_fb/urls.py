# File: mini_fb/urls.py
# Author: Kelley Han (kelhan@bu.edu), 2/18/25
# Description: URL patterns for the mini facebook application, includes Show All and individual profiles 

from django.urls import path 
from django.conf import settings 
from . import views 
from .views import *

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), #show all profiles
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='profile'), #Show singular profile
    path('create_profile', CreateProfileView.as_view(), name="create_profile"), 
    path('profile/<int:pk>/create_status', CreateStatusView.as_view(), name="create_status"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), 
]