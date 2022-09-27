
from django.shortcuts import render
from django.urls import path,include
from bitacora import views

urlpatterns = [
    path('', views.index, name='bitacora'),
    path('list/', views.list, name='bitacora_list'),
]