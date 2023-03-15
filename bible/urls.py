from django.urls import path
from . import views


urlpatterns = [
    # e.g. /bible/1/1/
    path('<int:book_id>/<int:chapter_id>/', views.index, name='index'),
]