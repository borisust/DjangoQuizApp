from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/register', views.registration, name='registration'),
    path('users/login', views.authentication, name='authentication')

]