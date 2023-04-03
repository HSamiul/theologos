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
        
        # prevent short cicuiting by doing this outside of the if-clause below
        # the entire form will be validated as a result
        userCreationFormValid = userCreationForm.is_valid()
        profileCreationFormValid = profileCreationForm.is_valid()
        
        if userCreationFormValid and profileCreationFormValid:
            user = userCreationForm.save()
            profile = profileCreationForm.save(commit=False) # generate user object without affecting database
            
            profile.user = user # create the profile's foreign key to user and save
            profile.save()
            
            messages.success(request, 'Account created successfully') # flash a success message
            return HttpResponse('Created user and profile!') # TODO: Redirect to homepage instead
        else:
            for error in profileCreationForm.errors:
                messages.error(request, profileCreationForm.errors[error])
                return redirect(request.path)
            for error in userCreationForm.errors:
                messages.error(request, userCreationForm.errors[error])
                return redirect(request.path)
            return HttpResponse('Failed to create user and profile :(') # TODO: give a more useful redirect
  
    # if this URL was requested via a GET method, display a form to register a user
    else:
        userCreationForm = UserCreationForm()
        profileCreationForm = ProfileCreationForm()
        
        context = {'userCreationForm' : userCreationForm,
                   'profileCreationForm' : profileCreationForm}
    
        return render(request, 'accounts/register.html', context)