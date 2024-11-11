from django.core.paginator import Paginator
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Reporte

def reporte_view(request):
    # Obtener el filtro de fecha desde la URL (por defecto es 'hoy')
    filtro = request.GET.get('filtro', 'hoy')
    
    # Obtener el término de búsqueda desde la URL (por defecto es una cadena vacía)
    query = request.GET.get('q', '')  # 'q' es el nombre del parámetro de búsqueda
    
    # Obtener la fecha actual
    hoy = datetime.now()
    
    # Filtrar según el criterio de fecha
    if filtro == 'hoy':
        fecha_inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)  # Comienza a las 00:00 de hoy
        fecha_fin = hoy.replace(hour=23, minute=59, second=59, microsecond=999999)  # Termina a las 23:59 de hoy
        reportes = Reporte.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
    elif filtro == 'mes':
        fecha_inicio = hoy - timedelta(days=hoy.day)  # Fecha del primer día del mes
        fecha_inicio = fecha_inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        reportes = Reporte.objects.filter(fecha__gte=fecha_inicio)
        
    elif filtro == 'año':
        fecha_inicio = hoy.replace(month=1, day=1)  # Primer día del año
        fecha_inicio = fecha_inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        reportes = Reporte.objects.filter(fecha__gte=fecha_inicio)
    
    # Si hay una búsqueda, filtrar también por el nombre o descripción
    if query:
        reportes = reportes.filter(nombre__icontains=query)  # Filtra los reportes por nombre que contengan 'query'
    
    # Paginación: dividir los reportes en páginas de 10 elementos
    paginator = Paginator(reportes, 10)  # 10 reportes por página
    
    # Obtener el número de la página actual
    page_number = request.GET.get('page')  # Esto puede ser pasado en la URL, como ?page=2
    page_obj = paginator.get_page(page_number)  # Obtener la página actual
    
    return render(request, 'reportes.html', {
        'page_obj': page_obj,
        'filtro': filtro,
        'query': query  # Pasamos el término de búsqueda al template
    })

#a