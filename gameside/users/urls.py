from django.urls import path

from . import views

app_name = 'users'


urlpattens = [path('', views.auth, name='auth')]
