# File: mini_fb/views.py
# Author: Kelley Han (kelhan@bu.edu), 2/18/25
# Description: includes the functions for views to show all profiles and show individual profiles 

from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm
# Create your views here.

class ShowAllProfilesView(ListView):
    '''subclass of listview to display all the user profiles'''
    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    '''subclass of detailview to display a single profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
