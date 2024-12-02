from django.urls import path, include
from . import views

app_name = 'reportes'

urlpatterns = [
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('envios/', views.lista_envios, name='lista_envios'),
    path('inventario/', views.lista_inventario, name='lista_inventario'),
]
