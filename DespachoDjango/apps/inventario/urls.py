from django.urls import path, include
from rest_framework import viewsets, permissions, routers
from apps.inventario.models import Product, Categoria
from apps.inventario.serializers import ProductSerializer, CategoriaSerializer
from django.urls import path
from . import views
from .views import (
    SeguimientoEnvioListView,
    SeguimientoEnvioCreateView,
    SeguimientoEnvioUpdateView
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]


router = routers.DefaultRouter()
router.register('productos', ProductViewSet)
router.register('categorias', CategoriaViewSet)

app_name = 'inventario'

urlpatterns = [
    path('', views.InventarioListView.as_view(), name='inventario_list'),
    path('productos/', views.ProductListView.as_view(), name='product_list'),
    path('producto/crear/', views.ProductCreateView.as_view(), name='product_create'),
    path('producto/<uuid:pk>/editar/',
         views.ProductUpdateView.as_view(), name='product_edit'),
    path('producto/<uuid:pk>/eliminar/',
         views.ProductDeleteView.as_view(), name='product_delete'),
    path('categorias/', views.CategoriaListView.as_view(), name='category_list'),
    path('categoria/crear/', views.CategoriaCreateView.as_view(),
         name='category_create'),
    path('categoria/<uuid:pk>/editar/',
         views.CategoriaUpdateView.as_view(), name='category_edit'),
    path('producto/<uuid:pk>/stock/',
         views.StockUpdateView.as_view(), name='stock_update'),
    path('seguimientos/', SeguimientoEnvioListView.as_view(),
         name='seguimiento_list'),
    path('seguimiento/crear/<uuid:orden_id>/',
         SeguimientoEnvioCreateView.as_view(), name='seguimiento_create'),
    path('seguimiento/<uuid:pk>/editar/',
         SeguimientoEnvioUpdateView.as_view(), name='seguimiento_update'),
    path('envios_activos/', views.envios_activos, name='envios_activos'),
    path('historial/', views.historial, name='historial'),
    # path('api/', include(router.urls)), #<-- Comente esta seccion porque la API no la estamos usando y no es necesaria para el proyecto -->
    path('exportar/', views.exportar_inventario, name='exportar_inventario'),

    path('configurar-reporte/', views.configurar_reporte,
         name='configurar_reporte'),

    path('listado-despacho/', views.OrdenDespachoListView.as_view(),
         name='listado_despacho'),
    path('orden-despacho/crear/',
         views.CrearOrdenDespachoView.as_view(), name='despacho_create'),

    # <-- Comente esta seccion porque cuando hice la url no esta realizada la seccion de los envios -->
    path('envios/<uuid:seguimiento_id>/cambiar_estado/',
         views.cambiar_estado_envio, name='cambiar_estado_envio'),

    path('configurar-reporte/', views.configurar_reporte,
         name='configurar_reporte'),
]
