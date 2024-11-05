from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
# mini_fb/views.py
# define views for mini_fb
# Create your views here.
from typing import Any
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import *
import random
from django.views import View
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.mixins import LoginRequiredMixin




# class-based view
class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''show /debug logged in user'''
        print(f'Logged in user: request.user={request.user}')
        print(f'Logged in user: request.user.is_authenticated={request.user.is_authenticated}')

        return super().dispatch(request, *args, **kwargs)

class ShowProfilePageView(DetailView):
    '''Show detailed profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    '''pick profile '''
    def get_object(self):
        '''Return one profile object '''
        if 'pk' in self.kwargs:
            return Profile.objects.get(pk=self.kwargs['pk'])
        else:
            return Profile.objects.get(user=self.request.user)
        
    def get_login_url(self):
        '''return URL required for login'''
        return reverse('mini_fb/login')
    
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
        
        return reverse('show_profile')
    

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
        # save the status message to database
        sm = form.save()
        # read the files from the form
        files = self.request.FILES.getlist('files')
        for file in files:
            # link img to status msg
            print(f"File {file}")
            img = Image(image_file=file, status_message=sm)
            img.save()

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''return URL to redirect after success'''
        return reverse('show_profile')
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''form to update profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        '''Return one profile object '''
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self) -> str:
        '''return URL to redirect after success'''

        return reverse('show_profile')
    


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''form to delete status'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    

    def get_success_url(self) -> str:
        '''return URL to redirect after success'''
        return reverse('show_profile')

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''form to update status'''
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'
    fields = ['message']

    def get_success_url(self) -> str:
        '''return URL to redirect after success'''
        #  returns to profile object
        return reverse('show_profile')
    
class CreateFriendView(LoginRequiredMixin, View):
    '''view for creating friend relationship'''


    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        other = Profile.objects.get(pk=self.kwargs['other_pk'])
        friendship = profile.add_friend(other)

        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    '''view to show friend suggestions'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self):
        '''Return one profile object '''
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Return one profile object '''
        return Profile.objects.get(user=self.request.user)