from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.InventarioListView.as_view(), name='inventario_list'),
    path('productos/', views.ProductListView.as_view(), name='product_list'),
    path('producto/crear/', views.ProductCreateView.as_view(), name='product_create'),
    path('producto/<uuid:pk>/editar/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('producto/<uuid:pk>/eliminar/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('categorias/', views.CategoriaListView.as_view(), name='category_list'),
    path('categoria/crear/', views.CategoriaCreateView.as_view(), name='category_create'),
    path('categoria/<uuid:pk>/editar/', views.CategoriaUpdateView.as_view(), name='category_edit'),
    path('producto/<uuid:pk>/stock/', views.StockUpdateView.as_view(), name='stock_update'),
    path('exportar/', views.exportar_inventario, name='exportar_inventario'),
    path('configurar-reporte/', views.configurar_reporte, name='configurar_reporte'),
    path('despachos/', views.DespachoListView.as_view(), name='despacho_list'),
    path('despacho/crear/', views.DespachoCreateView.as_view(), name='despacho_create'),
    path('despacho/<uuid:pk>/', views.DespachoDetailView.as_view(), name='despacho_detail'),
    path('despacho/<uuid:pk>/editar/', views.DespachoUpdateView.as_view(), name='despacho_edit'),
    path('despacho/<uuid:pk>/estado/', views.DespachoEstadoUpdateView.as_view(), name='despacho_estado'),
]