from apps.inventario.models import OrdenDespacho  # Importar el modelo desde la aplicación inventario
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from apps.inventario.models import OrdenDespacho

class ReporteView(ListView):
    model = OrdenDespacho
    template_name = 'reportes.html'
    context_object_name = 'ordenes_despacho'
    paginate_by = 5  # Número de objetos por página

    def get_queryset(self):
        # Obtiene el valor de búsqueda desde la URL (si existe)
        search_query = self.request.GET.get('search', '')

        queryset = OrdenDespacho.objects.select_related('cliente', 'cliente__cliente_profile','transportista')

        # Filtro de búsqueda por nombre de supermercado (insensible a mayúsculas/minúsculas)
        if search_query:
            queryset = queryset.filter(
                Q(cliente__cliente_profile__nombre_supermercado__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos el valor de búsqueda para que se mantenga en el campo del formulario
        context['search'] = self.request.GET.get('search', '')
        return context
