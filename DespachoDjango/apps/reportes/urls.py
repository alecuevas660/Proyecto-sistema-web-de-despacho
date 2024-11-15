# apps/reportes/urls.py

from django.urls import path
from .views import ReporteView

app_name = 'reportes'

urlpatterns = [
    # Aquí agrega las rutas específicas de la aplicación `reportes`
    path('', ReporteView.as_view(), name='reportes'),  # Esta es solo una ruta de ejemplo
]
