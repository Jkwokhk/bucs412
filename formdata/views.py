from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

# Create your views here.
def show_form(request):
    '''Show contact form'''
    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''
    Handle the form submission.
    Read the form data from the request
    and send it back to a template
    '''
    template_name = 'formdata/confirmation.html'
    # print(request)
    if request.POST:
    # read the form data into python variables
        name = request.POST['name']
        favorite_color = request.POST['color']
    

    # package the form data as context variables for the template

        context = {
            'name' : name,
            'favorite_color': favorite_color
        }
        return render(request, template_name, context)

# handle GET request on this URL
    template_name = 'formdata/form.html'
    return redirect(show_form)