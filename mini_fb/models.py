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
