from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutview, name='logout'),
]
