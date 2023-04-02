from django.urls import path
from . import views

urlpatterns = [
    # e.g. /bible/gen/1/
    path('<slug:book_id>/<int:chapter_num>/', views.index, name='index'), # serves as URL for many possible pages
    path('<slug:book_id>/<int:chapter_num>/<int:verse_num>/', views.index, name='index')
]