# blog/urls.py

from django.urls import path 
from django.conf import settings 
from . import views 
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), #show all profiles
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='profile'), #Show singular profile
]