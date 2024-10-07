from django.shortcuts import render
# mini_fb/views.py
# define views for mini_fb
# Create your views here.

from django.views.generic import ListView
from .models import *

# class-based view
class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
