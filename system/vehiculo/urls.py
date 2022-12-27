from django.urls import path
from system.vehiculo import views

urlpatterns = [
    path('', views.index, name='vehiculo'),
    path('list/', views.list, name='vehiculo_list'),
    path('insert/', views.insert, name='vehiculo_insert'),
    path('insertfile/', views.insertfile, name='vehiculo_insertfile'),
    path('update/', views.update, name='vehiculo_update'),
    path('state/', views.state, name='vehiculo_state'),
    path('delete/', views.delete, name='vehiculo_delete'),

    path('asignacion/', views.asignacion, name='vehiculo_asignacion'),
    path('retiro/', views.retiro, name='vehiculo_retiro'),
    path('transferir/', views.transferir, name='vehiculo_transferir'),

    path('categoriaList/', views.categoriaList, name='vehiculo_list'),
    path('categoriaInsert/', views.categoriaInsert, name='vehiculo_categoriaInsert'),
    path('categoriaUpdate/', views.categoriaUpdate, name='vehiculo_categoriaUpdate'),
    path('categoriaState/', views.categoriaState, name='vehiculo_categoriaState'),
    path('categoriaDelete/', views.categoriaDelete, name='vehiculo_categoriaDelete'),

]