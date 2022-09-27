from django.urls import path
from system.bitacora import views

urlpatterns = [
    path('', views.index, name='bitacora'),
    path('list/', views.list, name='bitacora_list'),
]