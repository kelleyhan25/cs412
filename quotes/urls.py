from django.urls import path 
from django.conf import settings 
from . import views 

urlpatterns = [
    path(r'', views.main_page, name="main_page"),
    path(r'quote/', views.main_page, name="quotes_page"),
    path(r'show_all/', views.show_all, name="show_all"),
    path(r'about/', views.about_page, name="about_page"),
]