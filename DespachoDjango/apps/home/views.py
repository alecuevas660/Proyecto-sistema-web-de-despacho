from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.inventario.models import Product, Categoria
from django.db.models import F, Count
import json
from datetime import datetime, timedelta

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas básicas
        productos = Product.objects.all()
        context['total_productos'] = productos.count()
        context['categorias_activas'] = Categoria.objects.filter(activo=True).count()
        
        # Productos con stock bajo (usando la misma lógica que en InventarioListView)
        productos_stock_bajo = []
        for producto in productos:
            stock_actual = producto.get_stock_actual()
            if stock_actual < producto.stock_minimo:
                productos_stock_bajo.append(producto)
        
        context['productos_stock_bajo'] = len(productos_stock_bajo)
        
        # Datos para gráficos (ejemplo con datos de prueba)
        context['labels_ventas'] = json.dumps(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'])
        context['datos_ventas'] = json.dumps([12, 19, 3, 5, 2, 3])
        
        context['labels_productos'] = json.dumps(['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'])
        context['datos_productos'] = json.dumps([12, 19, 3, 5, 2])
        
        # Datos de ejemplo para alertas y actividad
        context['alertas'] = [
            {
                'titulo': 'Stock Bajo',
                'mensaje': f'Hay {len(productos_stock_bajo)} productos que requieren reposición',
                'tipo': 'warning',
                'fecha': datetime.now() - timedelta(hours=2)
            },
            # Más alertas...
        ]
        
        context['actividades_recientes'] = [
            {
                'descripcion': 'Actualización de Stock',
                'detalles': 'Se actualizó el stock del producto X',
                'usuario': 'Admin',
                'fecha': datetime.now() - timedelta(minutes=30)
            },
            # Más actividades...
        ]
        
        return context
