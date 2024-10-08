# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import *
import random
# class-based view
class ShowAllView(ListView):
    '''the view to show all articles'''
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #context variable to use

class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'