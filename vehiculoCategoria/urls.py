
from django.shortcuts import render
from django.urls import path,include
from vehiculoCategoria import views

urlpatterns = [
    path('', views.index, name='vehiculoCategoria'),
    path('list/', views.list, name='vehiculoCategoria_list'),
    path('insert/', views.insert, name='vehiculoCategoria_insert'),
    path('update/', views.update, name='vehiculoCategoria_update'),
    path('state/', views.state, name='vehiculoCategoria_state'),
    path('delete/', views.delete, name='vehiculoCategoria_delete'),
]