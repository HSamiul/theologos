from django.urls import path
from .views import register, UserDetailView, UserUpdateView, UserDeleteView

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'), # /accounts/register/
    path('detail/', UserDetailView.as_view(), name='detail'), # /accounts/detail/
    path('edit/', UserUpdateView.as_view(), name='edit'), # /accounts/edit/
    path('delete/', UserDeleteView.as_view(), name='delete') # /accounts/delete/
]