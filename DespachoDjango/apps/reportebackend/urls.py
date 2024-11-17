# apps/reportes/urls.py

from django.urls import path
from .views import ReporteView

app_name = 'rreportebackend'

urlpatterns = [
    # Aquí agrega las rutas específicas de la aplicación `reportes`
    path('', ReporteView.as_view(), name='reportebackend'),  # Esta es solo una ruta de ejemplo
]
