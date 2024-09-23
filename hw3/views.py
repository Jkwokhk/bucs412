# hw3/views.py
# description: write view functions to handle URL requests for the web app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time
# Create your views here.
def home(request):
    '''
    Function to handle the URL request for /hw (main page)
    Delegate rendering to the template hw/ home.html
    '''
    # Use this template to render the response
    template_name = 'hw3/home.html'
    # create a dictionary of context variables for the template
    context = {
        "current_time": time.ctime(),
        'letter1' : chr(random.randint(65, 90)), # letter from A to Z
        'letter2' : chr(random.randint(65, 90)), # letter from A to Z
        'number' : random.randint(1,10),
    }
    # delegate rendering work to the template
    return render(request, template_name, context)
def about(request):
    '''
    Function to handle the URL request for /hw (main page)
    Delegate rendering to the template hw/ home.html
    '''
    # Use this template to render the response
    template_name = 'hw3/about.html'
    # create a dictionary of context variables for the template
    context = {
        "current_time": time.ctime(),
        'letter1' : chr(random.randint(65, 90)), # letter from A to Z
        'letter2' : chr(random.randint(65, 90)), # letter from A to Z
        'number' : random.randint(1,10),
    }
    # delegate rendering work to the template
    return render(request, template_name, context)
def quote(request):
    '''
    Function to handle the URL request for /hw (main page)
    Delegate rendering to the template hw/ home.html
    '''
    # Use this template to render the response
    template_name = 'hw3/quote.html'
    # create a dictionary of context variables for the template
    context = {
        "current_time": time.ctime(),
        'letter1' : chr(random.randint(65, 90)), # letter from A to Z
        'letter2' : chr(random.randint(65, 90)), # letter from A to Z
        'number' : random.randint(1,10),
    }
    # delegate rendering work to the template
    return render(request, template_name, context)
def show_all(request):
    '''
    Function to handle the URL request for /hw (main page)
    Delegate rendering to the template hw/ home.html
    '''
    # Use this template to render the response
    template_name = 'hw3/show_all.html'
    # create a dictionary of context variables for the template
    context = {
        "current_time": time.ctime(),
        'letter1' : chr(random.randint(65, 90)), # letter from A to Z
        'letter2' : chr(random.randint(65, 90)), # letter from A to Z
        'number' : random.randint(1,10),
    }
    # delegate rendering work to the template
    return render(request, template_name, context)