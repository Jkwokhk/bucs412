from django.db import models
from django.urls import reverse
from django.utils import timezone
# mini_fb/models.py
# Defining data objects
# Create your models here.

class Profile(models.Model):
    '''
    encapsulates the idea of one profile
    '''
    # data attributes of a profile
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} by {self.city}'
    
    def get_status_messages(self):
        '''return all status messages about this profile'''
        message = StatusMessage.objects.filter(profile=self)
        return message
    def get_absolute_url(self):
        # return url of this profile
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        # return list of friend's profiles
        profile1_friends = Friend.objects.filter(profile1 =self)
        profile2_friends = Friend.objects.filter(profile2=self)

        friends = [friend.profile2 for friend in profile1_friends] + [friend.profile1 for friend in profile2_friends]
        return friends

class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message in profile'''
    # data attributes of status message
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def get_images(self):
        return Image.objects.filter(status_message = self)

    def __str__(self):
        '''return string representation of this Status object'''
        return f'{self.message}'
    
    
class Image(models.Model):
    '''encapsulates the idea of an image in profile'''
    # data attributes of image
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        '''return str representation of this image object'''
        return f'{self.status_message} at {self.timestamp}'
    
class Friend(models.Model):
    '''encapsulates the idea of a friend(2 connecting nodes)'''
    # data attributes of friend
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        '''str representation of Friend'''
        return f"{self.profile1} and {self.profile2} at {self.timestamp}"