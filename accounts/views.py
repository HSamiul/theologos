from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def signup(request):
    template = loader.get_template('accounts/signup.html')
    
    # The empty dictionary would normally be a context dictionary.
    # It makes python variables available for use in the template file
    return HttpResponse(template.render({}, request))