# restaurant/view.py
# description: write view functions to handle URL requests for the web app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time
# Create your views here.
# Daily special items
specials = ['Chippy with Curry Sauce', 'Bombaclat', 'Peking Duck', 'Extra Hot Fire Chicken Noodles', 'Stargazy Pie', 'Bull Testies']
def main(request):
    template_name = 'restaurant/main.html'
    context = {

    }
    return render(request, template_name, context)

def order(request):
    template_name = 'restaurant/order.html'
    special = random.choice(specials)
    context = {
        'special': special,
    }
    return render(request, template_name, context)

def confirmation(request):
    template_name = 'restaurant/confirmation.html'
    context = {

    }
    return render(request, template_name, context)