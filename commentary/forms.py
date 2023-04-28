from django import forms
from .models import Post

'''
This is the form used by the bible:index view that allows users to add posts
'''
class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']