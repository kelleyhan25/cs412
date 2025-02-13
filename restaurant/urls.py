# File: urls.py 
# Author: Kelley Han (kelhan@bu.edu), 2/11/2025
# Description: URLS to view mapping for restaurant app 


from django.urls import path 
from django.conf import settings
from . import views 

#URL patterns for this app: 
urlpatterns = [
    path(r'main/', views.main_page, name='main_page'),
    path(r'', views.main_page, name='main_page'),
    path(r'order/', views.order_page, name='order_page'),
    path(r'confirmation', views.confirmation, name='confirmation'),
]