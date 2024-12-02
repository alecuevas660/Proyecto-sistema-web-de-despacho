# apps/reportes/urls.py

from django.urls import path
from .views import ReporteView
from . import views

app_name = 'rreportebackend'

urlpatterns = [
    path('', ReporteView.as_view(), name='reportebackend'), 
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
]
