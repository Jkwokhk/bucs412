from django.db import models
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
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} by {self.city}'
    
    def get_status_messages(self):
        '''return all status messages about this profile'''
        message = StatusMessage.objects.filter(profile=self)
        return message

class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message in profile'''
    # data attributes of status message
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''return string representation of this Status object'''
        return f'{self.message}'
    
    
    
