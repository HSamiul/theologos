from django.urls import path
from .views import register, UserDetailView

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'), # /accounts/register/
    path('<int:pk>/detail/', UserDetailView.as_view(), name='detail'), # /accounts/1/detail/
]