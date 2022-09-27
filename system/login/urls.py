from django.urls import path

from system.login import views


urlpatterns = [
path('', views.logon, name='login'),
path('logout/', views.signout, name='logout'),
]