from django.urls import path
from . import views

app_name = 'commentary'
urlpatterns = [
    path('<slug:pk>/detail', views.PostDetailView.as_view(), name='post-detail'), # i.e. /<post_id>/detail
    path('<slug:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'), # i.e. /<post_id>/delete
    path('<slug:pk>/edit', views.PostUpdateView.as_view(), name='post-edit'), # i.e. /<post_id>/edit
]