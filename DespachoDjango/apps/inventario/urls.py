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
]