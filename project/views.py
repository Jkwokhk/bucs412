# project/views.py
# define views for project
# Create your views here.
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
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
import plotly
import plotly.express as px
from django.utils.html import format_html
from django.db.models import Count

import plotly.graph_objs as go
from collections import Counter

# class based view
class ShowAllBoardGamesView(ListView):
    '''the view to show all board games'''
    model = BoardGame
    template_name = 'project/show_all_board_games.html'
    # to use in html
    context_object_name = 'board_games'

    def get_queryset(self):
        '''Filter board games by genre'''
        queryset = super().get_queryset()
        genre_filter = self.request.GET.get('genre')
        # filter by genre
        if genre_filter:
            queryset = queryset.filter(genre=genre_filter)

        # Filter by stock quantity (availability)
        stock_filter = self.request.GET.get('stock_quantity')
        if stock_filter == 'in_stock':
            queryset = queryset.filter(stock_quantity__gt=0)  # Games in stock
        elif stock_filter == 'out_of_stock':
            queryset = queryset.filter(stock_quantity=0)  # Games out of stock



        return queryset

    def get_context_data(self, **kwargs):
        '''Add available genres and selected genre to the context'''
        context = super().get_context_data(**kwargs)
        context['genres'] = dict(BoardGame.genres)  # Get available genres
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['selected_stock_quantity'] = self.request.GET.get('stock_quantity', '')
        return context


class ShowBoardGamePageView(DetailView):
    '''show details of board game'''
    model = BoardGame
    template_name = 'project/show_board_game.html'
    context_object_name = 'board_game'

    '''pick board game'''
    def get_object(self):
        '''return one board game object '''
        return BoardGame.objects.get(pk=self.kwargs['pk'])

class CreateBoardGameFormView(LoginRequiredMixin, CreateView):
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
    
class CreateRatingFormView(LoginRequiredMixin, CreateView):
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


class AddToCartViewForm(LoginRequiredMixin, CreateView):
    '''add a board game to the cart'''
    form_class = AddToCartForm
    template_name = 'project/add_to_cart_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board_game = BoardGame.objects.get(pk=self.kwargs['pk'])
        context['board_bame'] = board_game
        return context

    def form_valid(self, form):
        '''handle cart form submission'''
        customer = Customer.objects.get(user=self.request.user)
        # Check if the customer already has a cart order
        existing_order = Order.objects.filter(customer=customer, status='cart').first()
        # If an order already exists, use it; otherwise, create a new one
        if existing_order:
            order = existing_order
        else:
            order = Order.objects.create(customer=customer, status='cart')

        board_game = BoardGame.objects.get(pk=self.kwargs['pk'])
        form.instance.board_game = board_game
        form.instance.order = order

        return super().form_valid(form)
    
    def get_success_url(self):
        '''URL to redirect after successful form submission'''
        return reverse('show_all_board_games')
    
class ShowCartView(LoginRequiredMixin, ListView):
    '''display current items in cart'''
    model = OrderItem
    template_name = 'project/show_cart.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        '''filter cart items for current customer'''
        customer = Customer.objects.get(user=self.request.user)
        order = Order.objects.filter(customer=customer, status='cart').first()
        if order:
            # Return the related order items for that order
            return OrderItem.objects.filter(order=order)
        return OrderItem.objects.none()

    def get_context_data(self, **kwargs):
        '''Add total price to the context'''
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_price = sum(item.board_game.price * item.quantity for item in cart_items)
        context['total_price'] = total_price
        return context
    
class CheckoutView(LoginRequiredMixin, DetailView):
    '''handle order checkout/ decrease quantity in database and redirects to profile'''
    model = Order
    template_name = 'project/checkout.html'

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=self.request.user)
        order = get_object_or_404(Order, customer=customer, status='cart')
        
        # Start a transaction block
        with transaction.atomic():
            for item in order.order_items.all():
                board_game = item.board_game
                if board_game.stock_quantity < item.quantity:
                    return render(request, self.template_name, {
                        'error_message': f"Insufficient stock for {board_game.title}."
                    })
                board_game.stock_quantity -= item.quantity
                board_game.save()

            # Update order status to 'shipped'
            order.status = 'shipped'
            order.save()

        return redirect('show_profile')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''form to update profile'''
    model = Customer
    form_class = UpdateCustomerForm
    template_name = 'project/update_customer_form.html'

    def get_object(self):
        '''return one customer profile object'''
        return Customer.objects.get(user=self.request.user)
    
    def get_success_url(self):
        '''return URL to redirect after success'''
        return reverse('show_profile')

class DeleteRatingView(LoginRequiredMixin, DeleteView):
    '''form to delete rating'''
    model = Rating
    template_name = 'project/delete_rating_form.html'
    context_object_name = 'rating'

    def get_success_url(self):
        '''return URL to redirect after success'''
        return reverse('show_profile')

class CustomerGraphView(ListView):
    '''view for graph for customer analytics'''
    model = Customer
    template_name = 'project/graph.html'
    context_object_name = 'customers'

    def get_queryset(self):
        # Get orders with 'cart' or 'shipped' status
        queryset = Order.objects.filter(status__in=['cart', 'shipped'])
        
        # Optional: Apply filters based on GET parameters (e.g., for a specific time frame)
        # Example: if 'start_date' and 'end_date' are passed in the request:
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the orders to be processed
        orders = self.get_queryset()

        # Prepare data for the scatter plot
        customer_ages = []
        genres = []

        for order in orders:
            customer = order.customer
            if customer.age:  # Ensure the customer has an age
                customer_ages.append(customer.age)
            for item in order.order_items.all():
                board_game = item.board_game
                if board_game.genre:  # Ensure the board game has a genre
                    genres.append(board_game.genre)

        # Handle cases where data might be missing
        if not customer_ages or not genres:
            context['error'] = "No valid data available for plotting"
            return context

        # Scatter plot
        scatter_plot = go.Scatter(
            x=customer_ages,
            y=genres,
            mode='markers',
            marker=dict(size=12, color='rgba(51,204,255,0.6)', line=dict(width=1, color='rgba(51,204,255,1)')),
            text=genres,  # Show genre as hover text
            name='Customer Age vs Genre'
        )

        # Generate the Plotly graph as HTML
        graph = plotly.offline.plot({
            "data": [scatter_plot],
            "layout": go.Layout(
                title="Customer Age vs Board Game Genre",
                xaxis={'title': 'Customer Age'},
                yaxis={'title': 'Board Game Genre'},
                hovermode='closest'
            )
        }, auto_open=False, output_type='div')

        context['graph'] = graph  # Add the graph to context

        return context

class DeleteCartView(DeleteView):
    '''View to Delete Cart Items'''
    def post(self, request, *args, **kwargs):
        # Get the current logged-in user and their cart
        customer = Customer.objects.get(user=request.user)
        order = get_object_or_404(Order, customer=customer, status='cart')
        
        # Get the item to be deleted
        item_id = kwargs.get('item_id')
        item = get_object_or_404(OrderItem, id=item_id, order=order)
        
        # Delete the item
        item.delete()
        
        order.save()
        
        return redirect('show_profile')  # Redirect back to the profile or cart page