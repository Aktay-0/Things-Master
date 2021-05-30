from django.contrib import admin
from django.urls import path
from . import views
from .mqtt import client

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('device/', views.device, name='device'),
    path('device-register/', views.device_register, name='device_register'),
    path('profile/', views.profile, name='profile'),
    path('save_config/', views.save_config, name='save_config'),
]

client.loop_start()