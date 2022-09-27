
from django.shortcuts import render
from django.urls import path,include
from rol import views

urlpatterns = [
    path('', views.index, name='rol'),
    path('list/', views.list, name='rol_list'),
    path('insert/', views.insert, name='rol_insert'),
    path('update/', views.update, name='rol_update'),
    # path('state/', views.state, name='rol_state'),
    # path('delete/', views.delete, name='rol_delete'),
]