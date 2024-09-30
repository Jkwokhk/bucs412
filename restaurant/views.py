# restaurant/view.py
# description: write view functions to handle URL requests for the web app
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random, datetime
# Create your views here.
# Daily special items and menu items
extras = {
        'Extra Crispy': 1,
        'Extra Cream': 2,
        'Extra Stuffing': 2,
    }
menu = {
        'Orange Chicken': 10,
        'Seasame Chicken': 12,
        'Kung Pao Chicken': 8,
        'Crab Rangoons': 4,
    }
specials = ['Chippy with Curry Sauce', 'Bombaclat', 'Peking Duck', 'Extra Hot Fire Chicken Noodles', 'Stargazy Pie', 'Bull Testies']
def main(request):
    template_name = 'restaurant/main.html'
    context = {

    }
    return render(request, template_name, context)

def order(request):
    template_name = 'restaurant/order.html'
    special = random.choice(specials)
    request.session['special'] = special
    
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
        special = request.session.get('special')
        special_instructions = request.POST['special_instructions']
        ordered_extras = request.POST.getlist('extras')
        ordered_items = request.POST.getlist('menu')
        extra_price = sum(extras[item] for item in ordered_extras if item in extras)
        total_price = sum(menu[item] for item in ordered_items if item in menu)
        ordered_special = 'special' in request.POST
        if(ordered_special):
            total_price += 15
        total_price = total_price + extra_price
        
        ready_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 60))
        ready_time_str = ready_time.strftime("%H:%M")
        context = {
            
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ordered_items': ordered_items,
            'ready_time': ready_time_str,
            'special': special,

        }
        return render(request, template_name, context)
    
    template_name = 'restaurant/order.html'
    return redirect(order)

