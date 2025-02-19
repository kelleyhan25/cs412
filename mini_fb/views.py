from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView 
# Create your views here.

class ShowAllProfilesView(ListView):
    '''subclass of listview to display all the user profiles'''
    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'