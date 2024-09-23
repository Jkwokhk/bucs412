# hw3/urls.py
# description: URL patterns for the hw app
from django.urls import path
from django.conf import settings
from . import views

# All urls that are part of this app
urlpatterns = [
    path(r'', views.quote, name="quote"),
    path(r'quote', views.quote, name="quote"),
    path(r'about', views.about, name="about"),
    path(r'show_all', views.show_all, name="show_all"),
    
]