from django.shortcuts import render
# mini_fb/views.py
# define views for mini_fb
# Create your views here.
from typing import Any
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
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

    '''pick profile '''
    def get_object(self):
        '''Return one profile object '''
        pk = self.kwargs.get('pk')
        print("pk is")
        print(pk)
        return Profile.objects.get(pk=pk)
    
class CreateProfileForm(CreateView):
    '''a view to create a new profile and save it to database'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     '''
    #     Build the dict of context data for this view
    #     '''
    #     # superclass context data
    #     context = super().get_context_data(**kwargs)
    #     # find pk from URL
    #     pk = self.kwargs['pk']
    #     # find corresponding profile
    #     profile = Profile.objects.get(pk=pk)
    #     # add profile to context data
    #     context['profile'] = profile


    #     return context

    def form_valid(self, form):
        '''
        Handle the form submission
        '''
        # print(form.cleaned_data)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        '''return URL to redirect after submit successfully'''
        
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    

class CreateStatusMessageView(CreateView):
    '''a form to create status for profile'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''handle form submission'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        print(self.kwargs)
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''return URL to redirect after success'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    




