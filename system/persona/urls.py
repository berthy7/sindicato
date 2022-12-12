
from django.shortcuts import render
from django.urls import path,include
from system.persona import views

urlpatterns = [
    path('', views.index, name='persona'),
    path('list/', views.list, name='persona_list'),
    path('listAll/', views.listAll, name='persona_listAll'),
    path('<int:id>/', views.obtain, name='persona_obtain'),
    path('insert/', views.insert, name='persona_insert'),
    path('insertfile/', views.insertfile, name='persona_insertfile'),
    path('update/', views.update, name='persona_update'),
    path('state/', views.state, name='persona_state'),
    path('delete/', views.delete, name='persona_delete'),
    path('reporte/<int:id>/', views.reporte, name='persona_reporte'),
    path('listarPersonaXTipo/<str:id>/', views.listarPersonaXTipo, name='persona_listarPersonaXTipo'),

    path('agregarInternos/', views.agregarInternos, name='persona_agregarInternos'),
    path('eliminarInternos/<int:id>', views.eliminarInternos, name='persona_eliminarInternos'),

    path('agregarReferencia/', views.agregarReferencia, name='persona_agregarReferencia'),
    path('modificarReferencia/', views.modificarReferencia, name='persona_modificarReferencia'),
    path('eliminarReferencia/<int:id>', views.eliminarReferencia, name='persona_eliminarReferencia'),

]