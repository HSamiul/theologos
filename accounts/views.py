from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':  
        form = UserCreationForm(request.POST) # create form with POST data
        
        if form.is_valid():
            form.save()  
        messages.success(request, 'Account created successfully')  
  
    else:  
        form = UserCreationForm()  
    context = {  
        'form':form,
    }  
    return render(request, 'accounts/register.html', context)