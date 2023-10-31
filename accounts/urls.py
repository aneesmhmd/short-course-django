from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('dashboard/', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile-page'),
    path('change-password/', change_password, name="change-password"),
]
