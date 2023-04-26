import django_filters
from django import forms
from profiles.models import FaithTradition

# filter form used in Bible split view to filter comments according to faith tradition
class PostFilter(django_filters.FilterSet):
    faith_tradition = django_filters.MultipleChoiceFilter(
        field_name='author__faith_tradition',
        choices=FaithTradition.choices,
        widget=forms.CheckboxSelectMultiple
    )