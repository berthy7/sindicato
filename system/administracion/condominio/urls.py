
from django.shortcuts import render
from django.urls import path,include
from system.administracion.condominio import views

urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.home, name='home'),
# path('signup/', views.signup, name='signup'),
# path('logout/', views.signout, name='logout'),
# path('signin/', views.signin, name='signin'),
#
# path('condominio/', include(('system.administracion.condominio.urls','condominio'))),

path('', views.condominio, name='condominio'),
path('create/', views.create_condominio, name='create_condominio'),
path('<int:id>/', views.condominio_detalle, name='condominio_detalle'),
# path('condominio/<int:id>/eliminar/', views.condominio_eliminar, name='condominio_eliminar')

]