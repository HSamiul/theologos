from typing import Any, Optional
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
# from django.contrib.auth.decorators import user_passes_test

from profiles.forms import ProfileForm
from .forms import UserCreationForm
from .models import User

# @user_passes_test
class UserDetailView(DetailView):
    model = User
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object()
        return context
    
    def get_object(self):
        # TODO: Add a helpful message instead of just 404'ing
        return get_object_or_404(User, id=self.request.user.id)
    
class UserUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name_suffix = "_update_form"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["profile"] = user.profile
        context["profileForm"] = ProfileForm(instance=user.profile)
        return context
    
    def form_valid(self, form):
        user = self.get_object()
        profileUpdateForm = ProfileForm(self.request.POST, instance=user.profile)
        
        # need to check profile form separately
        if profileUpdateForm.is_valid():
            profileUpdateForm.save()
            messages.success(self.request, 'Account updated successfully')
            context = { 'object' : user, 'profile' : user.profile }
            return render(self.request, 'accounts/user_detail.html', context)
        else:
            for error in profileUpdateForm.errors:
                messages.error(self.request, profileUpdateForm.errors[error])
                return redirect(self.request.path)
            return HttpResponse('Failed to update account :(')
    
    def get_success_url(self):
        return reverse_lazy("accounts:detail", kwargs={"pk":self.get_object().pk})
    
    def test_func(self):
        user = self.get_object()
        return self.request.user.pk == user.pk


class UserDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = User
    success_url = reverse_lazy("login")

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
            
            messages.success(request, 'Account created successfully. Please try logging in.') # flash a success message
            return redirect("home")
        else:
            for error in profileForm.errors:
                messages.error(request, profileForm.errors[error])
                
            for error in userCreationForm.errors:
                messages.error(request, userCreationForm.errors[error])
                
            return redirect(request.path) # TODO: prefill form with the existing data so user doesn't have to start over
  
    # if this URL was requested via a GET method, display a form to register a user
    else:
        if request.user.is_authenticated:
            messages.error(request, "You cannot register an account while signed in.")
            return redirect("home")
        
        userCreationForm = UserCreationForm()
        profileForm = ProfileForm()
        
        context = {'userCreationForm' : userCreationForm,
                   'profileForm' : profileForm}
    
        return render(request, 'accounts/register.html', context)