from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .models import Profile
from .forms import ProfileCreationForm

def profile(request):
    if request.method == 'POST':
        # profile = Profile.objects.get(user=request.user)
        # form = ProfileCreationForm(request.POST, instance=profile)
        form = ProfileCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile created successfully')
            return HttpResponse('Created your profile!')
    else:
        form = ProfileCreationForm()

    return render(request, 'profiles/profiles.html', {'form': form})
