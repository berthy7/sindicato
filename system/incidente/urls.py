
from django.shortcuts import render
from django.urls import path,include
from system.incidente import views

urlpatterns = [
    path('', views.index, name='incidente'),
    path('list/', views.list, name='incidente_list'),
    path('insert/', views.insert, name='incidente_insert'),
    path('update/', views.update, name='incidente_update'),
    path('state/', views.state, name='incidente_state'),
    path('delete/', views.delete, name='incidente_delete'),

    path('tipoList/', views.tipoList, name='incidente_list'),
    path('tipoInsert/', views.tipoInsert, name='incidente_tipoInsert'),
    path('tipoUpdate/', views.tipoUpdate, name='incidente_tipoUpdate'),
    path('tipoState/', views.tipoState, name='incidente_tipoState'),
    path('tipoDelete/', views.tipoDelete, name='incidente_tipoDelete'),

]