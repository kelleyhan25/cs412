# voter_analytics/urls.py
# Kelley Han kelhan@bu.edu 
# This file contains the URL mappings to the views for voter_analytics 
from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VotersListView.as_view(), name='voters'),
    path(r'voters/', views.VotersListView.as_view(), name='voters_list'),
    path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter_detail'),
    path(r'graphs/', views.GraphDataListView.as_view(), name="graphs"),
]