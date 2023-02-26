from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    # if this URL was requested via a POST method, try creating a user
    if request.method == 'POST': 
        form = UserCreationForm(request.POST) # use POST data to create a form
        
        if form.is_valid():
            form.save()  
            messages.success(request, 'Account created successfully') # flash a success message
            return HttpResponse('Created your account!')
  
    # otherwise, display a form to register a user
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})