from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from profiles.forms import ProfileCreationForm
from .forms import UserCreationForm

def register(request):
    # if this URL was requested via a POST method, try creating a user
    if request.method == 'POST': 
        # use POST data to populate forms
        userCreationForm = UserCreationForm(request.POST)
        profileCreationForm = ProfileCreationForm(request.POST)
        
        userCreationFormValid = userCreationForm.is_valid()
        profileCreationFormValid = profileCreationForm.is_valid()
        
        if userCreationFormValid and profileCreationFormValid:
            user = userCreationForm.save()
            profile = profileCreationForm.save(commit=False)
            
            profile.user = user
            profile.save()
            
            messages.success(request, 'User and profile created successfully') # flash a success message
            return HttpResponse('Created user and profile!')
  
    # otherwise, display a form to register a user
    else:
        userCreationForm = UserCreationForm()
        profileCreationForm = ProfileCreationForm()
        
        context = {'userCreationForm' : userCreationForm,
                   'profileCreationForm' : profileCreationForm}
    
    return render(request, 'accounts/register.html', context)