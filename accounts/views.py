from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if (request.POST == 'POST'):
        form = UserCreationForm()
        
        if form.is_valid(): # how could it not be valid if I'm instiating it myself?
            form.save()
    else:
        form = UserCreationForm()
    
    context = { 'form': form }
    
    return render(request, 'accounts/register.html', context)