# mini_fb/urls.py
# description: URL patterns for the fb app
from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

# All urls that are part of this app
urlpatterns = [
    
    path('', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile_with_pk'),
    path('create_profile/', CreateProfileForm.as_view(), name='create_profile'),
    path('profile/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update/', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete/',DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update',UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]