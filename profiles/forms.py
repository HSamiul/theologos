from django.forms import ModelForm
from django import forms
from .models import Profile

class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'faith_tradition', 'phone']
        
        # override the default textfield type of dob to be a datepicker instead
        widgets = {
            'dob' : forms.DateInput(attrs={'type': 'date'})
        }
