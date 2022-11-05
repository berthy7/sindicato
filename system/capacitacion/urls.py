
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

    path('cursoList/', views.cursoList, name='capacitacion_cursoList'),
    path('cursoInsert/', views.cursoInsert, name='capacitacion_cursoInsert'),
    path('cursoUpdate/', views.cursoUpdate, name='capacitacion_cursoUpdate'),
    path('cursoState/', views.cursoState, name='capacitacion_cursoState'),
    path('cursoDelete/', views.cursoDelete, name='capacitacion_cursoDelete'),

]