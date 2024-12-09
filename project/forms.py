# project/forms.py

from django import forms
from .models import *

class CreateBoardGameForm(forms.ModelForm):
    '''a form to add a Board Game to the database'''
    class Meta:
        model = BoardGame
        '''associated fields'''
        fields =['title', 'publisher', 'release_year', 'price', 'stock_quantity', 'image_url', 'genre']

class CreateRatingForm(forms.ModelForm):
    '''a form to add Rating to the database'''
    class Meta:
        model = Rating
        fields = ['board_game', 'comment', 'rating']

class CreateCustomerForm(forms.ModelForm):
    '''a form to add a Customer Profile to the database'''
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'age']
