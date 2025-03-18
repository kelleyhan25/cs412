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
    path('create_profile', CreateProfileView.as_view(), name="create_profile"), #create profile form
    path('profile/<int:pk>/create_status', CreateStatusView.as_view(), name="create_status"), #create status message form
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), #update profile form 
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"), #delete status message form 
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"), #update status message form 
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'), #add friends
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), #friend suggestions page
    path('profile/<int:pk>/news_feed',ShowNewsFeedView.as_view(), name="news_feed"), #show news feed 
]