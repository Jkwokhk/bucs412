# mini_fb/forms.py
from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''a form to add a profile to database'''
    class Meta:
        '''associate this form with the Profile model; select fields'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

