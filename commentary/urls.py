from django.urls import path
from . import views

app_name = 'commentary'
urlpatterns = [
    path('post/<slug:pk>', views.PostDetailView.as_view(), name='post-detail'), # i.e. /post/<post_id>
    path('post/<slug:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'), # i.e. /post/<post_id>/delete
]