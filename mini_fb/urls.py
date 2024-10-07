# mini_fb/urls.py
# description: URL patterns for the fb app
from django.urls import path
from django.conf import settings
from . import views

# All urls that are part of this app
urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
]