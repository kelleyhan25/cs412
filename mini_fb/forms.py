from django import forms
from .models import Profile, StatusMessage
from django.forms import TextInput
class CreateProfileForm(forms.ModelForm):

    '''A form to add a profile to the database.'''

    class Meta: 
        '''associate the form with a model from the database'''
        model = Profile 
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url',]

class CreateStatusMessageForm(forms.ModelForm):
    '''a form to add status messages to the database.'''

    class Meta: 
        model = StatusMessage
        fields = ['message',]
       