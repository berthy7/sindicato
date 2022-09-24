
from django.shortcuts import render
from django.urls import path,include
from system.bus import views

urlpatterns = [
    path('', views.index, name='bus'),
    path('list/', views.list, name='bus_list'),
    path('insert/', views.insert, name='bus_insert'),
    path('update/', views.update, name='bus_update'),
    path('state/', views.state, name='bus_state'),
    path('delete/', views.delete, name='bus_delete'),
]