# project/views.py
# define views for project
# Create your views here.
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from typing import Any
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import *
import random
from django.views import View
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.models import User

# class based view
class ShowAllBoardGamesView(ListView):
    '''the view to show all board games'''
    model = BoardGame
    template_name = 'project/show_all_board_games.html'
    # to use in html
    context_object_name = 'board_games'


class ShowBoardGamePageView(DetailView):
    '''show details of board game'''
    model = BoardGame
    template_name = 'project/show_board_game.html'
    context_object_name = 'board_game'

    '''pick board game'''
    def get_object(self):
        '''return one board game object '''
        return BoardGame.objects.get(pk=self.kwargs['pk'])

class CreateBoardGameFormView(CreateView):
    '''a view to create a board game form and save to database'''
    form_class = CreateBoardGameForm
    template_name = 'project/create_board_game_form.html'
    
    def form_valid(self, form):
        '''handle form submission'''
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''URL to redirect after successful form submission'''
        # return reverse('game', kwargs={'pk': self.kwargs['pk']})
        return reverse('show_board_game_with_pk', kwargs={'pk': self.object.pk})
    
class CreateRatingFormView(CreateView):
    '''a view to create a rating form and save to database'''
    form_class = CreateRatingForm
    template_name = 'project/create_rating_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board_game = BoardGame.objects.get(pk=self.kwargs['pk'])
        context['board_game'] = board_game
        return context
    
    def form_valid(self, form):
        '''handle rating form submission'''
        # assign current customer to current user
        form.instance.customer =  Customer.objects.get(user=self.request.user)
        # assign board game
        
        board_game = BoardGame.objects.get(pk=self.kwargs['pk'])
        form.instance.board_game = board_game
        return super().form_valid(form)
    
    def get_success_url(self):
        '''return URL to redirect after success'''
        return reverse('show_board_game_with_pk', kwargs={'pk': self.kwargs['pk']})
    

class CreateCustomerProfileFormView(CreateView):
    '''a view to create a new profile and save to database'''
    '''for now admin will also use this form'''
    form_class = CreateCustomerForm
    template_name = 'project/create_profile_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''handle form submission'''
        new_user_form = UserCreationForm(self.request.POST)
        if new_user_form.is_valid():
            user = new_user_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        '''return URL to redirect after successful submission'''
        return reverse('show_profile')
    

class ShowProfilePageView(DetailView):
    '''show detailed profile'''
    model = Customer
    template_name = 'project/show_profile.html'
    context_object_name = 'customer'

    '''pick profile'''
    def get_object(self):
        # print(self.kwargs)
        if 'pk' in self.kwargs:
            print('other profiles')
            return Customer.objects.get(pk=self.kwargs['pk'])
        else:
            return Customer.objects.get(user=self.request.user)


