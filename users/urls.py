from django.urls import path

from .views import (
	UserCreateAPIView,
	UserLoginAPIView,
    UserDetailAPIView
)

app_name = 'users-api'
urlpatterns = [
    path('register', UserCreateAPIView.as_view()),
    path('login', UserLoginAPIView.as_view()),
    path('info',UserDetailAPIView.as_view())
]
