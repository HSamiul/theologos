from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm

def profile(request):
    if request.method == 'POST':
        # profile = Profile.objects.get(user=request.user)
        # form = ProfileForm(request.POST, instance=profile)
        form = ProfileForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile created successfully')
            return HttpResponse('Created your profile!')
    else:
        form = ProfileForm()

    return render(request, 'profiles/profiles.html', {'form': form})
