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
    
    def get_friends(self):
        '''return all friends of this profile'''
        friends1 = Friend.objects.filter(profile1=self) 
        friends2 = Friend.objects.filter(profile2=self)
        friends_list = []
        for friend in friends1:
            friends_list.append(friend.profile2)
        for friend2 in friends2: 
            friends_list.append(friend2.profile1)
        return friends_list 
    
    def add_friend(self, other):
        '''check if friends exist and add if they don't. '''
        if self == other: 
            return 
        friend_exists1 = Friend.objects.filter(profile1=self, profile2=other)
        friend_exists2 = Friend.objects.filter(profile1=other, profile2=self)

        if (len(friend_exists1) == 0 and len(friend_exists2) == 0):
            friend = Friend(profile1=self, profile2=other)
            friend.save()

    def get_friend_suggestions(self):
        '''returns a list of possible friends for a profile.'''
        current_friends = self.get_friends()
        if not current_friends: 
            return []
        #print("current friends: ", current_friends)
        friend_suggestions = []
        excluded_profiles = [self]
    
        excluded_profiles.extend(current_friends)

        for friend in current_friends: 
            friends_of_friend = friend.get_friends()
        #print("friends of friends", friends_of_friend)
        
        for possible_friend in friends_of_friend:
            if possible_friend not in excluded_profiles:
                friend_suggestions.append(possible_friend)
                excluded_profiles.append(possible_friend)
        #print("friend suggestions", friend_suggestions)
        return friend_suggestions
    
    def get_news_feed(self):
        '''shows status messages for each of the friends of a given user'''
        my_friends = self.get_friends()
        all_messages = StatusMessage.objects.filter(profile__in=my_friends).order_by('-time_stamp')
        print(all_messages)
        return all_messages

 
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


class Friend(models.Model):
    '''Encapsulate the idea of a Friend of a Profile.'''

    #data attributes of a Friend: 
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now="True")

    def __str__(self):
        '''Returns a string representation of the Friends'''
        return f'{self.profile1} & {self.profile2}'
