from DespachoDjango.apps.ventas.models import Venta, DetalleVenta
from django.template.loader import render_to_string

def generar_reporte_venta(venta_id):
    # Obtener la venta
    venta = Venta.objects.get(id=venta_id)
    cliente = venta.cliente_profile.nombre_supermercado
    asignado = venta.vendedor.get_full_name()
    
    # Obtener los detalles de la venta desde el modelo DetalleVenta
    detalles = []
    total_venta = 0
    for detalle in venta.detalles.all():  # Esto es un queryset de DetalleVenta
        detalles.append({
            'producto': detalle.producto.name,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.precio_unitario,
            'subtotal': detalle.subtotal
        })
        total_venta += detalle.subtotal  # Sumamos el subtotal de cada producto
    
    # Crear el reporte de venta
    reporte = {
        'cliente': cliente,
        'asignado': asignado,
        'detalles': detalles,
        'total_venta': total_venta
    }
    return reporte
