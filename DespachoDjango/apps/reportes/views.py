from django.views.generic import TemplateView
from apps.inventario.models import OrdenDespacho  # Importar el modelo desde la aplicación inventario
from django.shortcuts import render

class ReporteView(TemplateView):
    template_name = 'reportes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todas las órdenes de despacho y añadir los datos al contexto
        ordenes_despacho = OrdenDespacho.objects.select_related('cliente', 'transportista').all()
        print(ordenes_despacho)
        
        # Añadir las órdenes al contexto
        context['ordenes_despacho'] = ordenes_despacho
        
        return context

