from django import forms
from .models import Profile

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'faith_tradition', 'phone']
        
        # override the default textfield type of dob to be a datepicker instead
        widgets = {
            'dob' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'faith_tradition': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
