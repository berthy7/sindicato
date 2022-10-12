"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from system.login import views


urlpatterns = [
    path('admin/', admin.site.urls),
path('', views.home, name='home'),

path('login/', include(('system.login.urls', 'system.login'))),

path('vehiculo/', include(('system.vehiculo.urls', 'system.vehiculo'))),
path('vehiculoCategoria/', include(('system.vehiculoCategoria.urls', 'system.vehiculoCategoria'))),
path('linea/', include(('system.linea.urls', 'system.linea'))),

path('persona/', include(('system.persona.urls', 'system.persona'))),
path('conductor/', include(('system.conductor.urls', 'system.conductor'))),
path('incidente/', include(('system.incidente.urls', 'system.incidente'))),
# path('evento/', include(('system.evento.urls', 'system.evento'))),


path('usuario/', include(('system.usuario.urls', 'system.usuario'))),
path('rol/', include(('system.rol.urls', 'system.rol'))),
path('bitacora/', include(('system.bitacora.urls', 'system.bitacora'))),

]
