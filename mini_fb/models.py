from django.db import models

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