from django.forms import ModelForm
from django.contrib.auth.models import User

# RegistrationForm subclasses ModelForm
class RegistrationForm(ModelForm):
    # Metadata about RegistrationForm; anything that's not a field
    class Meta:
        model = User
        fields = ['username', 'password']