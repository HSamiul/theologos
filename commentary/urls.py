from django.urls import path
from . import views

app_name = 'commentary'
urlpatterns = [
    # e.g. /commentary/<post_id>/delete/
    path('<slug:pk>/delete/', views.PostDeleteView.as_view(), name='delete-post'),

    # e.g. /commentary/<post_id>/edit/
    path('<slug:pk>/edit/', views.PostUpdateView.as_view(), name='edit-post'),

    # TODO: Add delete comment URL and view
]