from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # e.g. /bible/phil/1/1/
    path('<slug:book_symbol>/<int:chapter_num>/<int:verse_num>/', views.index, name='index')
]