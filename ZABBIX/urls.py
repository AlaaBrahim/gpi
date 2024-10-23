# zabbixapp/urls.py
from django.urls import path
from . import views

urlpatterns = [

 
    path('ajouter_hote/', views.ajouter_hote, name='ajouter_hote'),
   
   
    path('test/', views.test, name='test'),
]
