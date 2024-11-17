
from decimal import Decimal
from django.shortcuts import redirect, render
from apps.inventario.models import Categoria, Product
from django.utils import timezone
from datetime import datetime, timedelta
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl import Workbook
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

def reporte_inventario(request):
    # Obtener filtros del request
    nombre = request.GET.get('nombre', '')
    categoria_id = request.GET.get('categoria')
    stock_status = request.GET.get('stock_status')
    fecha_filtro = request.GET.get('fecha_filtro')

    # Filtrar productos activos
    productos = Product.objects.filter(activo=True)

    # Filtro de nombre
    if nombre:
        productos = productos.filter(name__icontains=nombre)

    # Filtro de categoría
    if categoria_id:
        productos = productos.filter(categoria__id=categoria_id)

    # Filtro de estado de stock
    if stock_status:
        productos = [p for p in productos if p.get_stock_status()[1] == stock_status]

    # Filtro de fecha
    if fecha_filtro == 'hoy':
        productos = productos.filter(created_at__date=timezone.now().date())
    elif fecha_filtro == 'ultimo_mes':
        productos = productos.filter(created_at__gte=timezone.now() - timedelta(days=30))
    elif fecha_filtro == 'ultimo_ano':
        productos = productos.filter(created_at__gte=timezone.now() - timedelta(days=365))

    # Crear lista de productos con stock y valores calculados
    productos_inventario = []
    total_valor_inventario = 0

    for producto in productos:
        stock_actual = producto.get_stock_actual()
        valor_inventario = producto.price * stock_actual
        total_valor_inventario += valor_inventario

        productos_inventario.append({
            'producto': producto,
            'stock_actual': stock_actual,
            'valor_inventario': valor_inventario,
            'stock_status': producto.get_stock_status()
        })

    # Pasar datos y categorías para los filtros al template
    categorias = Categoria.objects.all()

    # Verificar si se solicita descargar el PDF
    if 'descargar_pdf' in request.GET:
        return #generar_pdf_reporte_inventario(request, productos_inventario, total_valor_inventario, categorias)
    
    # Verificar si se solicita descargar el Excel
    if 'descargar_excel' in request.GET:
        return #generar_excel_reporte_inventario(productos_inventario, total_valor_inventario)

    # Renderizar el reporte en la vista HTML normal
    return render(request, 'reportes/reporte_inventario.html', {
        'productos_inventario': productos_inventario,
        'total_valor_inventario': total_valor_inventario,
        'categorias': categorias,
    })

def reporte_general_inventario(): #Plantilla para realizar reporte general
    productos = Product.objects.filter(activo=True)
    reporte_data = []
    total_valor_inventario = Decimal('0.00')

    for producto in productos:
        stock_actual = producto.get_stock_actual()
        stock_status, stock_status_class = producto.get_stock_status()
        valor_total_producto = producto.price * stock_actual

        reporte_data.append({
            'nombre': producto.name,
            'categoria': producto.categoria.name,
            'precio': producto.price,
            'stock_minimo': producto.stock_minimo,
            'stock_actual': stock_actual,
            'estado_stock': stock_status,
            'valor_total': valor_total_producto,
        })

        total_valor_inventario += valor_total_producto

    return reporte_data, total_valor_inventario

def reporte_por_categoria_inventario(categoria_id): #Plantilla para realizar reporte por categoria
    categoria = Categoria.objects.get(id=categoria_id)
    productos = categoria.productos.filter(activo=True)
    reporte_data = []
    total_valor_inventario = Decimal('0.00')

    for producto in productos:
        stock_actual = producto.get_stock_actual()
        stock_status, stock_status_class = producto.get_stock_status()
        valor_total_producto = producto.price * stock_actual

        reporte_data.append({
            'nombre': producto.name,
            'descripcion': producto.description,
            'precio': producto.price,
            'stock_minimo': producto.stock_minimo,
            'stock_actual': stock_actual,
            'estado_stock': stock_status,
            'valor_total': valor_total_producto,
        })

        total_valor_inventario += valor_total_producto

    return reporte_data, total_valor_inventario

def reporte_bajos_en_stock_inventario(): #Plantilla para realizar reporte bajos en stock
    productos = Product.objects.filter(activo=True)
    reporte_data = []
    total_valor_inventario = Decimal('0.00')

    for producto in productos:
        stock_actual = producto.get_stock_actual()
        if stock_actual < producto.stock_minimo * 0.30:  # Si el stock es menor al 30% del stock mínimo
            stock_status, stock_status_class = producto.get_stock_status()
            valor_total_producto = producto.price * stock_actual

            reporte_data.append({
                'nombre': producto.name,
                'categoria': producto.categoria.name,
                'precio': producto.price,
                'stock_minimo': producto.stock_minimo,
                'stock_actual': stock_actual,
                'estado_stock': stock_status,
                'valor_total': valor_total_producto,
            })

            total_valor_inventario += valor_total_producto

    return reporte_data, total_valor_inventario

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

