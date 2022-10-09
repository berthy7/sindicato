from django.urls import path
from system.vehiculo import views

urlpatterns = [
    path('', views.index, name='vehiculo'),
    path('list/', views.list, name='vehiculo_list'),
    path('insert/', views.insert, name='vehiculo_insert'),
    path('update/', views.update, name='vehiculo_update'),
    path('state/', views.state, name='vehiculo_state'),
    path('delete/', views.delete, name='vehiculo_delete'),

    path('asignacion/', views.asignacion, name='vehiculo_asignacion'),
    path('retiro/', views.retiro, name='vehiculo_retiro'),
]