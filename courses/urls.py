from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('list/', list_courses,name='list'),
    path('add/', add_new_course,name='add-course'),
    path('delete/<int:id>/', delete_course,name='delete-course'),
    path('update-status/<int:id>/', update_status,name='update-status'),
    path('edit-course/<int:id>/', edit_course,name='edit-course'),
    path('search-courses/', search_course,name='search-course'),
]
