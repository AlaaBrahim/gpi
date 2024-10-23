from django.urls import path
from . import views
from .views import import_excel
from .views import export_materiel_to_excel

urlpatterns = [
  path('', views.index, name='index'),
  path('materiel/<int:id>/', views.view_materiel, name='view_materiel'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('import_excel/', import_excel, name='import_excel'),
  path('export_excel/', export_materiel_to_excel, name='export_excel'),
  path('', views.index, name='index'), 
  
]
