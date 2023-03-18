from django.forms import ModelForm
from .models import Profile

# TODO: Create a form that combines the User and Profile models.
class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'faith_tradition', 'phone']
