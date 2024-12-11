# project/urls.py
# Jason Kwok U35429106
# description: URL patterns for the terrier_games app
from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

# All urls that are part of this app
urlpatterns = [ 

    path('', views.ShowAllBoardGamesView.as_view(), name="show_all_board_games"),
    path('game/<int:pk>/', views.ShowBoardGamePageView.as_view(), name='show_board_game_with_pk'),
    path('create_board_game/', CreateBoardGameFormView.as_view(), name='create_board_game'),
    path('game/<int:pk>/create_rating', CreateRatingFormView.as_view(), name='create_rating'),
    path('rating/delete_rating/<int:pk>', DeleteRatingView.as_view(), name='delete_rating'),
    path('create_profile/', CreateCustomerProfileFormView.as_view(), name='create_profile'),
    path('profile/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    path('game/<int:pk>/add_to_cart/', AddToCartViewForm.as_view(), name='add_to_cart'),
    path('show_cart/', ShowCartView.as_view(), name='show_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('graph/', CustomerGraphView.as_view(), name='graph'),
    path('show_cart/delete_cart/<int:item_id>/', DeleteCartView.as_view(), name='delete_cart'),

    
]