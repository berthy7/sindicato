
from django.shortcuts import render
from django.urls import path,include
from system.chat import views

urlpatterns = [
    path('', views.index, name='chat'),
    path('<int:id>/', views.obtain, name='chat_obtain'),
    path('home/', views.home, name='chat_home'),
    path('list/', views.list, name='chat_list'),
    path('insert/', views.insert, name='chat_insert'),
    path('update/', views.update, name='chat_update'),
    path('delete/', views.delete, name='chat_delete'),

]