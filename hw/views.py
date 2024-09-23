# hw/views.py
# description: write view functions to handle URL requests for the hw app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time, random
# Create your views here.
# def home(request):
#     '''Handle the main URL for the hw app'''
#     response_text = f'''
#     <html>
#     <h1>Hello World!</h1>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>
#     '''

#     # create and return a response to client
#     return HttpResponse(response_text)

def home(request):
    '''
    Function to handle the URL request for /hw (main page)
    Delegate rendering to the template hw/ home.html
    '''
    # Use this template to render the response
    template_name = 'hw/home.html'
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
    template_name = 'hw/about.html'
    # create a dictionary of context variables for the template
    context = {
        "current_time": time.ctime(),
        'letter1' : chr(random.randint(65, 90)), # letter from A to Z
        'letter2' : chr(random.randint(65, 90)), # letter from A to Z
        'number' : random.randint(1,10),
    }
    # delegate rendering work to the template
    return render(request, template_name, context)