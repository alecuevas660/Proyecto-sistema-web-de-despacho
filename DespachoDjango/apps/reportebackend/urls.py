# apps/reportes/urls.py

from django.urls import path
from .views import ReporteView
from . import views

app_name = 'rreportebackend'

urlpatterns = [
<<<<<<< HEAD
    path('', ReporteView.as_view(), name='reportebackend'), 
=======
    # Aquí agrega las rutas específicas de la aplicación `reportes`
    path('', ReporteView.as_view(), name='reportebackend'),  # Esta es solo una ruta de ejemplo
>>>>>>> a78dd5d0da9c93d7f98d1c059e1ae4fdb6bc8298
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
]
