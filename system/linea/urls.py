
from django.shortcuts import render
from django.urls import path,include
from system.linea import views

urlpatterns = [
    path('', views.index, name='linea'),
    path('list/', views.list, name='linea_list'),
    path('insert/', views.insert, name='linea_insert'),
    path('insertfile/', views.insertfile, name='linea_insertfile'),
    path('update/', views.update, name='linea_update'),
    path('state/', views.state, name='linea_state'),
    path('delete/', views.delete, name='linea_delete'),
    path('agregarInternos/', views.agregarInternos, name='linea_agregarInternos'),
    path('mapa/', views.mapa, name='linea_mapa'),

    path('listarInternosXLinea/<int:id>/', views.listarInternosXLineaNoVehiculo, name='linea_listarInternosXLinea'),

    path('listarTodoInternosXLinea/<int:id>/', views.listarTodoInternosXLinea, name='linea_listarTodoInternosXLinea'),

]