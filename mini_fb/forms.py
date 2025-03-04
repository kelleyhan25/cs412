from django import forms
from .models import Profile, StatusMessage
from django.forms import TextInput
class CreateProfileForm(forms.ModelForm):

    '''A form to add a profile to the database.'''
    first_name = forms.CharField(label="First Name",required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)

    class Meta: 
        '''associate the form with a model from the database'''
        model = Profile 
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url',]

class CreateStatusMessageForm(forms.ModelForm):
    '''a form to add status messages to the database.'''

    class Meta: 
        model = StatusMessage
        fields = ['message',]

class UpdateProfileForm(forms.ModelForm):
    '''add a form to update the profile in the database.'''

    class Meta: 
        model = Profile
        fields = ['city', 'email_address', 'profile_image_url',]
       