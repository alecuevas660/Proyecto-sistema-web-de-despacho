from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.inventario.models import Product, Categoria, StockVariable
from apps.users.models import User
from datetime import timedelta

class HomeView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard"""
    template_name = 'dashboard/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Obtener datos reales del inventario
        productos = Product.objects.all()
        productos_stock_bajo = [p for p in productos if p.get_stock_actual() < p.stock_minimo]
        
        # Obtener últimos cambios de stock
        ultimos_cambios_stock = StockVariable.objects.select_related(
            'producto'
        ).order_by('-id')[:5]  # Usamos id para ordenar por más reciente
        
        # Datos para el dashboard
        context.update({
            'title': 'Dashboard',
            'total_productos': productos.count(),
            'categorias_activas': Categoria.objects.filter(activo=True).count(),
            'productos_stock_bajo': len(productos_stock_bajo),
            'total_clientes': User.objects.filter(role='client').count(),
            
            # Alertas basadas en productos con stock bajo
            'alertas': [
                {
                    'titulo': f'Stock Bajo en {p.name}',
                    'mensaje': f'El producto está por debajo del mínimo requerido ({p.stock_minimo} unidades)',
                    'tipo': 'warning',
                    'fecha': now
                }
                for p in productos_stock_bajo[:5]  # Mostrar solo las 5 primeras alertas
            ],
            
            # Datos para los gráficos
            'labels_productos': [p.name for p in productos[:5]],
            'datos_productos': [p.get_stock_actual() for p in productos[:5]],
            
            # Actividad reciente basada en cambios de stock
            'actividades_recientes': [
                {
                    'descripcion': f'Actualización de stock: {cambio.producto.name}',
                    'detalles': f'Nuevo stock: {cambio.cantidad_stock} unidades. Motivo: {cambio.motivo}',
                    'usuario': cambio.producto.categoria.nombre if cambio.producto.categoria else 'Sin categoría',
                    'fecha': now - timedelta(hours=i)  # Simulamos fechas recientes
                }
                for i, cambio in enumerate(ultimos_cambios_stock)
            ] if ultimos_cambios_stock else [],

            # Datos adicionales para las tarjetas del dashboard
            'ordenes_pendientes': 0,  # Esto se actualizará cuando tengamos el modelo de órdenes
            'ordenes_hoy': 0,
            'ventas_dia': 0,
            'porcentaje_incremento': 0,
        })
        
        return context
