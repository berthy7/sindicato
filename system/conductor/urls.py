
from django.shortcuts import render
from django.urls import path,include
from system.conductor import views

urlpatterns = [
    path('', views.index, name='conductor'),
    path('form/<int:id>/', views.form, name='conductor_form'),
    path('list/', views.list, name='conductor_list'),
    path('listAll/', views.listAll, name='persona_listAll'),
    path('reporte/<int:id>/', views.reporte, name='persona_reporte')

]