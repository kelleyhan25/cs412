# File: mini_fb/models.py
# Author: Kelley Han kelhan@bu.edu 2/18/25
# Description: includes the Profiles model for facebook profile, includes data attributes

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''Encapsulates the facebook profile of a user'''

    # data attributes of a profile
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Returns string representation of this Profile user name'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''Return all of the status messages on this profile.'''

        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        '''return the URL to display show an instance of the profile'''
        return reverse('profile', kwargs={'pk':self.pk})

class StatusMessage(models.Model):
    '''Encapsulates the Facebook status message.'''

    # data attributes of StatusMessage 
    time_stamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Returns a string representation of the StatusMessage'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all of the status messages on this profile.'''

        #status_images = StatusImage.objects.filter(status_message=self)
        images = Image.objects.filter(statusimage__status_message=self)
        return images
    

class Image(models.Model):
    '''Encapsulates the idea of an image file '''

    # data atrributes of an Image 
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Returns a string representation of the Image'''
        return f'{self.caption}'


class StatusImage(models.Model):
    '''encapsulates the idea of a status image'''

    # data attributes of a StatusImage 
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        '''Returns a string representation of the StatusImage'''
        return f'{self.status_message}'
