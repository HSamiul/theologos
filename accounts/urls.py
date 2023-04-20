from django.urls import path
from .views import register, UserDetailView, UserUpdateView, UserDeleteView

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'), # /accounts/register/
    path('<int:pk>/detail/', UserDetailView.as_view(), name='detail'), # /accounts/1/detail/
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='edit'), # /accounts/1/edit/
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete') # /accounts/1/delete/
]