# File: mini_fb/views.py
# Author: Kelley Han (kelhan@bu.edu), 2/18/25
# Description: includes the functions for views to show all profiles and show individual profiles 

from django.shortcuts import render, redirect
from .models import Profile, StatusMessage, StatusImage, Image
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
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
    '''subclass of createview to display the form for creating a profile'''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['usercreationform'] = UserCreationForm()
        return context 
    
    def form_valid(self, form):
        '''reconstruct usercreationform instance from the self.request.POST data'''
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save() 
        form.instance.user = user

        return super().form_valid(form)
    
class CreateStatusView(LoginRequiredMixin, CreateView):
    '''subclass of createview to display the form for creating a status message'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_object(self):
        '''method for object lookup in URL w/out pk'''
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        #pk = self.kwargs['pk']
        #profile = Profile.objects.get(pk=pk)
        profile = self.get_object()
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(profile=profile)
            image.image_file = file
            image.save()

            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
    def get_context_data(self):
        context = super().get_context_data()
        #pk = self.kwargs['pk']
        #profile = Profile.objects.get(pk=pk)
        context['profile'] = self.get_object()
        user = self.request.user
        context['user'] = user
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':pk})
    
    def get_login_url(self):
        return reverse('login')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''subclass of updateview to display the form for updating a profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    def get_object(self):
        '''method for object lookup in URL w/out pk'''
        return Profile.objects.get(user=self.request.user)

    
    def get_login_url(self):
        return reverse('login')
    def form_valid(self, form):
        user = self.request.user 
        form.instance.user = user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        context['user'] = user 
        return context 
    def get_success_url(self):
        #pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':self.object.pk})
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''a view to delete a status message and remove it from the database.'''
    template_name = 'mini_fb/delete_status_form.html'
    model = StatusMessage
    context_object_name = 'status_message'

    def get_success_url(self):
        '''returns the URL that we should be redirected to after deletion'''
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk)
        profile = status_message.profile
        return reverse('profile', kwargs={'pk':profile.pk})
    def get_login_url(self):
        return reverse('login')
    def form_valid(self, form):
        user = self.request.user 
        form.instance.user = user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        context['user'] = user 
        return context 

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''a view to update the status message text and update the database.'''
    form_class = UpdateStatusForm
    template_name = 'mini_fb/update_status_form.html'
    model = StatusMessage

    def get_login_url(self):
        return reverse('login')
    
    def form_valid(self, form):
        user = self.request.user 
        form.instance.user = user
        return super().form_valid(form)
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['status_message'] = status_message
        user = self.request.user
        context['user'] = user
        return context
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk)
        profile = status_message.profile
        return reverse('profile', kwargs={'pk':profile.pk})
    
class AddFriendView(LoginRequiredMixin, View):
    '''a view to add a friend to a profile.'''
    def get_object(self):
        '''method for object lookup in URL w/out pk'''
        return Profile.objects.get(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        #pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']

        #profile = Profile.objects.get(pk=pk)
        profile = self.get_object()
        friendProfile = Profile.objects.get(pk=other_pk)
        profile.add_friend(friendProfile)
        return redirect(reverse('profile', kwargs={'pk':profile.pk}))
    
    def get_login_url(self):
        return reverse('login')
    
    def form_valid(self, form):
        user = self.request.user 
        form.instance.user = user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        context['user'] = user 
        return context 
    
class ShowFriendSuggestionsView(DetailView):
    '''a view to show friend suggestions page'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    def get_object(self):
        '''method for object lookup in URL w/out pk'''
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''a view to display all status messages of a user's friends'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    def get_object(self):
        '''method for object lookup in URL w/out pk'''
        return Profile.objects.get(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        news_feed = profile.get_news_feed()
        print(news_feed)
        context['news_feed'] = news_feed
        user = self.request.user 
        context['user'] = user 
        return context
    
    def get_login_url(self):
        return reverse('login')
    
    def form_valid(self, form):
        user = self.request.user 
        form.instance.user = user
        return super().form_valid(form)