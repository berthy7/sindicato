
from django.shortcuts import render
from django.urls import path,include
from system.conductor import views

urlpatterns = [
    path('', views.index, name='conductor'),
    path('list/', views.list, name='conductor_list'),
    path('reporte/<int:id>/', views.reporte, name='persona_reporte')

]