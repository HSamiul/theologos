from django.urls import path
from . import views

app_name = 'bible'

urlpatterns = [
    path('', views.BibleCommentaryView.as_view(), name='index'), # e.g. /bible
    path('<slug:verse_id>', views.BibleCommentaryView.as_view(), name='index'), # e.g. /bible/gen-001-001
]