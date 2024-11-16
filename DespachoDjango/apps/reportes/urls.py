from django.urls import path, include
from . import views

app_name = 'reportes'

urlpatterns = [
    path('ventas/lista/', views.lista_ventas, name='lista_ventas'),
]
