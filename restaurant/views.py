# restaurant/view.py
# description: write view functions to handle URL requests for the web app
from django.shortcuts import render, redirect
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
    menu = [
        {'name': "Orange Chicken", 'price': 10},
        {'name': "Kung Pao Chicken", 'price': 8},
        {'name': "Seasame Chicken", 'price': 12},
        {'name': "Crab Rangoon", 'price': 2},
    ]
    extras = [
        {'topping': "Extra Crispy", 'price': 1},
        {'topping': "Extra Cream", 'price': 1},
        {'topping': "Extra Stuffing", 'price': 1.5},
    ]
    context = {
        'special': special,
        'menu': menu,
        'extras': extras,
    }
    return render(request, template_name, context)

def confirmation(request):
    template_name = 'restaurant/confirmation.html'
    # read the form data into python variables
    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST['special_instructions']
        items_ordered = []
        total_price = 0
        for item in request.POST:
            if item in ['name', 'phone','email','special_instructions']:
                continue
            print(item)
            item_price = 5
            # item_price = float(request.POST[item].price) if request.POST[item].price else 0
            items_ordered.append((item, item_price))
            total_price += item_price
            ready = time.localtime 
        context = {
            'items_ordered': items_ordered,
            'total_price': total_price,
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions

        }
        return render(request, template_name, context)
    
    template_name = 'restaurant/order.html'
    return redirect(order)

