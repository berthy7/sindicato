from django.urls import path
from system.usuario import views

urlpatterns = [
    path('', views.index, name='usuario'),
    path('list/', views.list, name='usuario_list'),
    path('listar/', views.listar, name='usuario_listar'),
    path('insert/', views.insert, name='usuario_insert'),
    path('update/', views.update, name='usuario_update'),
    path('delete/', views.delete, name='usuario_delete'),
    path('account/', views.account, name='usuario_account'),

    path('changepassword/', views.changepassword, name='usuario_changepassword'),
]