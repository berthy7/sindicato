
from django.shortcuts import render
from django.urls import path,include
from system.administracion.domicilio import views

urlpatterns = [

path('', views.index, name='domicilio'),
path('form/', views.form, name='domicilio_form'),
path('list/', views.list, name='domicilio_list'),
path('state/', views.state, name='domicilio_state'),
path('delete/', views.delete, name='domicilio_delete'),

]