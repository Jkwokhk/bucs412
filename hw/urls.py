# hw/urls.py
# description: URL patterns for the hw app
from django.urls import path
from django.conf import settings
from . import views

# All urls that are part of this app
urlpatterns = [
    path(r'', views.home, name="home"),
    path(r'about', views.about, name="about"),
    
]