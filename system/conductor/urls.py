
from django.shortcuts import render
from django.urls import path,include
from system.conductor import views

urlpatterns = [
    path('', views.index, name='conductor'),
    path('list/', views.list, name='conductor_list'),
    path('insert/', views.insert, name='conductor_insert'),
    path('update/', views.update, name='conductor_update'),
    path('state/', views.state, name='conductor_state'),
    path('delete/', views.delete, name='conductor_delete'),
]