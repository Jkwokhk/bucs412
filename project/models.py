
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your models here.
class BoardGame(models.Model):
    '''encapsulates the idea of a boardgame'''
    genres = [
        ('strategy', 'Strategy'),
        ('family', 'Family'),
        ('party', 'Party'),
        ('wargame', 'Wargame'),
        ('detective', 'Detective'),
        ('roleplay', 'Roleplay'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    release_year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=20, choices=genres)
    stock_quantity = models.IntegerField()
    image_url = models.URLField(max_length=500)
    # might change to image instead of url 

    def get_absolute_url(self):
        return reverse('game', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title
    
    def get_ratings(self):
        '''return all ratings'''
        rating = Rating.objects.filter(board_game = self)
        return rating
    
    

# Customer model
class Customer(models.Model):
    '''encapsulates the idea of a customer'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    age = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def get_absolute_url(self):
        # return url of this profile
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_rating_messages(self):
        '''returns ratings from current customer'''
        message = Rating.objects.filter(customer = self)
        return message
    
    def get_orders(self):
        '''return all orders'''
        orders = Order.objects.filter(customer = self, status__in=['shipped', 'delivered'])
        order_items = []
        # Here im getting all order items that associate with the order
        for order in orders:
            order_items.extend(order.order_items.all())
        return order_items

# Order model
class Order(models.Model):
    '''encapsulates the idea of an order'''
    status = [
        ('cart', 'Cart'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    order_date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status)
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"

# OrderItem model
class OrderItem(models.Model):
    '''encapsulates the idea of an ordered item'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    board_game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.quantity} x {self.board_game.title}"

# Rating model
class Rating(models.Model):
    '''encapsulates the idea of a rating system'''
    board_game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    def __str__(self):
        return f"Rating for {self.board_game.title} by {self.customer.first_name}"
    
