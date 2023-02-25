from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST': # if this URL was requested via a POST method...
        form = UserCreationForm(request.POST) # create form with the POST data
        
        if form.is_valid(): # validate and save the form (account)
            form.save()  
            messages.success(request, 'Account created successfully') # Flash a success message
            return HttpResponse('Created your account!') # TODO: Redirect to account page
  
    else:  # URL was requested via GET, so just display the form
        form = UserCreationForm()  
        
    context = {  
        'form':form,
    }
      
    return render(request, 'accounts/register.html', context)