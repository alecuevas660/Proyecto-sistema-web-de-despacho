from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.inventario.models import Product
from apps.ventas.models import Venta
from django.db.models import F, Count

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener estadísticas
        context['total_productos'] = Product.objects.count()
        context['productos_bajos'] = Product.objects.filter(
            stock_variables__cantidad_stock__lte=F('stock_minimo')
        ).distinct().count()
        
        # Alertas
        alertas = []
        productos_bajos = Product.objects.filter(
            stock_variables__cantidad_stock__lte=F('stock_minimo')
        ).distinct()
        
        for producto in productos_bajos:
            alertas.append({
                'tipo': 'warning',
                'mensaje': f'Stock bajo para "{producto.name}". Stock actual: {producto.get_stock_actual()}'
            })
        
        context['alertas'] = alertas
        
        return context
