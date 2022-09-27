from django.urls import path
from system.usuario import views

urlpatterns = [
    path('', views.index, name='usuario'),
    path('list/', views.list, name='usuario_list'),
    path('insert/', views.insert, name='usuario_insert'),
    path('update/', views.update, name='usuario_update'),
    path('delete/', views.delete, name='usuario_delete'),
]