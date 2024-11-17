from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from apps.inventario.models import OrdenDespacho
from openpyxl import Workbook
from django.http import HttpResponse
from django.utils import timezone
from xhtml2pdf import pisa
from django.template.loader import render_to_string
class ReporteView(ListView):
    model = OrdenDespacho
    template_name = 'reportebackend.html'
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
    
def exportar_excel(request):
    
    queryset = OrdenDespacho.objects.select_related('cliente', 'cliente__cliente_profile','transportista')
    # Crear el libro de Excel
    wb = Workbook()
    ws_reporte = wb.active
    ws_reporte.title = "Reporte Financiero"

    # Agregar parámetros del reporte
    ws_reporte.append(['REPORTE FINANCIERO'])
    ws_reporte.append(['Id de la orden', 'Cliente', 'Asignado a'])

    for orden in queryset:
        # Añadir una fila con los datos correspondientes
        cliente_nombre = orden.cliente.cliente_profile.nombre_supermercado if orden.cliente and orden.cliente.cliente_profile else "N/A"
        transportista_nombre = orden.transportista.get_full_name() if orden.transportista else "N/A"
        
        ws_reporte.append([str(orden.id), cliente_nombre, transportista_nombre])


    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Reporte_financiero_{}.xlsx'.format(
        timezone.now().strftime('%Y%m%d_%H%M%S')
    )

    wb.save(response)
    return response
    #return HttpResponse("¡La función exportar_excel ha sido ejecutada!")


def exportar_pdf(request):
    # Obtén los datos de las órdenes de despacho
    queryset = OrdenDespacho.objects.select_related('cliente', 'cliente__cliente_profile', 'transportista')

    # Convertimos los UUIDs a cadenas (si es necesario)
    ordenes_data = []
    for orden in queryset:
        orden_id_str = str(orden.id)  # Convertimos el UUID a string
        cliente_nombre = orden.cliente.cliente_profile.nombre_supermercado
        asignado_a = orden.transportista.get_full_name() if orden.transportista else 'N/A'
        
        ordenes_data.append({
            'id': orden_id_str,
            'cliente': cliente_nombre,
            'asignado_a': asignado_a
        })

    # Renderizamos el HTML a partir de una plantilla
    html_content = render_to_string('reporte_pdf_template.html', {'ordenes': ordenes_data})

    # Creamos una respuesta HTTP con el contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ordenes.pdf"'

    # Usamos xhtml2pdf para generar el PDF a partir del HTML
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    # Si hubo un error al generar el PDF, retornamos un mensaje
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=400)

    return response