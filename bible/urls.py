from django.urls import path
from . import views

app_name = 'bible'

urlpatterns = [
    path('', views.BibleCommentaryView.as_view(), name='index'),
    # e.g. /bible/gen/1/ or /bible/gen/1/1/
    path('<slug:book_symbol>/<int:chapter_num>/<int:verse_num>/', views.BibleCommentaryView.as_view(), name='index'),
    path('<slug:book_symbol>/<int:chapter_num>/<int:verse_num>/<int:post_id>', views.BibleCommentaryView.as_view(), name='index')
]