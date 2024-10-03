# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *

# class-based view
class ShowAllView(ListView):
    '''the view to show all articles'''
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #context variable to use