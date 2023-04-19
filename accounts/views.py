from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from profiles.forms import ProfileForm
from .forms import UserCreationForm
from .models import User

class UserDetailView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = User
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object().profile
        return context
    
    def test_func(self):
        user = self.get_object()
        return self.request.user.pk == user.pk
    


def register(request):
    # if this URL was requested via a POST method, try creating a user
    if request.method == 'POST': 
        # use POST data to populate forms
        userCreationForm = UserCreationForm(request.POST)
        profileForm = ProfileForm(request.POST)
        
        # prevent short circuiting by doing this outside of the if-clause below
        # the entire form will be validated as a result
        userCreationFormValid = userCreationForm.is_valid()
        profileFormValid = profileForm.is_valid()
        
        if userCreationFormValid and profileFormValid:
            user = userCreationForm.save()
            profile = profileForm.save(commit=False) # generate user object without affecting database
            
            profile.user = user # create the profile's foreign key to user and save
            profile.save()
            
            messages.success(request, 'Account created successfully') # flash a success message
            return HttpResponse('Created user and profile!') # TODO: Redirect to homepage instead
        else:
            for error in profileForm.errors:
                messages.error(request, profileForm.errors[error])
                return redirect(request.path)
            for error in userCreationForm.errors:
                messages.error(request, userCreationForm.errors[error])
                return redirect(request.path)
            return HttpResponse('Failed to create user and profile :(') # TODO: give a more useful redirect
  
    # if this URL was requested via a GET method, display a form to register a user
    else:
        userCreationForm = UserCreationForm()
        profileForm = ProfileForm()
        
        context = {'userCreationForm' : userCreationForm,
                   'profileForm' : profileForm}
    
        return render(request, 'accounts/register.html', context)