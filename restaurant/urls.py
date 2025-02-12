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