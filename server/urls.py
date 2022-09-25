"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from system.administracion.condominio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

path('login/', include(('system.login.urls','login'))),
path('condominio/', include(('system.administracion.condominio.urls','condominio'))),
path('domicilio/', include(('system.administracion.domicilio.urls','domicilio'))),

# path('usuario/', include(('system.seguridad.usuario.urls','usuario'))),

path('usuario/', include(('system.usuario.urls','usuario'))),

path('bus/', include(('system.bus.urls','bus'))),
path('linea/', include(('system.linea.urls','linea'))),
path('conductor/', include(('system.conductor.urls','conductor')))


]
