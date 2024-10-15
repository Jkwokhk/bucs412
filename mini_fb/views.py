from django.shortcuts import render
# mini_fb/views.py
# define views for mini_fb
# Create your views here.

from django.views.generic import ListView, DetailView
from .models import *
import random

# class-based view
class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''Show detailed profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    '''pick profile at random'''
    def get_object(self):
        '''Return one profile object chosen randomly'''
        all_profiles = Profile.objects.all()
        return random.choice(all_profiles)
