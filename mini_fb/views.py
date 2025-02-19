from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView
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
