# File: mini_fb/views.py
# Author: Kelley Han (kelhan@bu.edu), 2/18/25
# Description: includes the functions for views to show all profiles and show individual profiles 

from django.shortcuts import render
from .models import Profile, StatusMessage
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
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
    def get_context_data(self, **kwargs):  #i attempted to do this without the **kwargs, but it wouldn't show. so i used the default get_context_data that filled in on vscode including the **kwargs
        context = super().get_context_data(**kwargs)
        context['form'] = CreateStatusMessageForm()
        return context


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
class CreateStatusView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_context_data(self):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':pk})
