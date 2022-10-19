
from django.shortcuts import render
from django.urls import path,include
from system.capacitacion import views

urlpatterns = [
    path('', views.index, name='capacitacion'),
    path('list/', views.list, name='capacitacion_list'),
    path('insert/', views.insert, name='capacitacion_insert'),
    path('update/', views.update, name='capacitacion_update'),
    path('state/', views.state, name='capacitacion_state'),
    path('delete/', views.delete, name='capacitacion_delete'),
]