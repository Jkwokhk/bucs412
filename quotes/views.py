# hw3/views.py
# description: write view functions to handle URL requests for the web app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time
# Create your views here.
# All the quotes here as a global variable
quotes = [
    "One good thing about music, when it hits you you feel no pain",
    "The good times of today, are the sad thoughts of tomorrow",
    "Money can't buy life",
    "Every man gotta right to decide his own destiny",
    "When one door is closed, don't you know, another one is open"
]
# All the images here as a global variable
images = [
    "https://i.ytimg.com/vi/CoabDBD1N2Q/hqdefault.jpg?sqp=-oaymwEmCOADEOgC8quKqQMa8AEB-AH-BIAC4AOKAgwIABABGBEgcigkMA8=&rs=AOn4CLAdSw2p3OtYbALu5h3r4Kw3bMrX1g",
    "https://hips.hearstapps.com/hmg-prod/images/gettyimages-78683778.jpg?crop=0.988xw:0.988xh;0.0119xw,0.0119xh&resize=640:*",
    "https://www.rollingstone.com/wp-content/uploads/2018/06/rs-193885-541070899.jpg?w=1581&h=1054&crop=1",
    "https://media.gq-magazine.co.uk/photos/5e3af120318f780008ca687b/master/pass/20191126-bob-marley-11.jpg",
    "https://www.dancehallmag.com/assets/2024/01/Bob-Marley.jpg"
]

def about(request):
    '''
    Function to handle the URL request for /quotes (main page)
    Delegate rendering to the template quotes/ about.html
    '''
    # Use this template to render the response
    template_name = 'quotes/about.html'
    # create a dictionary of context variables for the template
    context = {

    }
    # delegate rendering work to the template
    return render(request, template_name, context)
def quote(request):
    '''
    Function to handle the URL request for /hw3 (main page)
    Delegate rendering to the template hw3/ quote.html
    '''
    # Use this template to render the response
    template_name = 'quotes/quote.html'
    # Selecting a random quote and image 
    quote = random.choice(quotes)
    image = random.choice(images)
    # create a dictionary of context variables for the template
    context = {
        'quote': quote,
        'image': image
    }
    # delegate rendering work to the template
    return render(request, template_name, context)
def show_all(request):
    '''
    Function to handle the URL request for /hw3 (main page)
    Delegate rendering to the template hw3/ show_all.html
    '''
    # Use this template to render the response
    template_name = 'quotes/show_all.html'
    # create a dictionary of context variables for the template
    context = {
        'quotes': [{'quote':quotes[i]} for i in range(len(quotes))],
        'images':[{'image':images[i]} for i in range(len(images))],
    }
    # delegate rendering work to the template
    return render(request, template_name, context)

