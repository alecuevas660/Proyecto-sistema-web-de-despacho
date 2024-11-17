from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.inventario.models import Product, Categoria, StockVariable, DetalleCompra
from apps.ventas.models import Product, DetalleVenta
from apps.users.models import User
from datetime import timedelta
from django.db.models import Sum
from apps.ventas.models import Venta

class HomeView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard"""
    template_name = 'dashboard/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # Obtener las ventas del día actual
        monto_ventas_dia = Venta.objects.filter(fecha_venta__day=now.day).aggregate(Sum('total'))['total__sum'] or 0
        # Convertir el monto a un valor entero
        monto_ventas_dia = int(monto_ventas_dia)

        # Obtener las ventas del día anterior
        ayer = now - timedelta(days=1)
        monto_ventas_ayer = Venta.objects.filter(fecha_venta__day=ayer.day).aggregate(Sum('total'))['total__sum'] or 0
        monto_ventas_ayer = int(monto_ventas_ayer)

        # Calcular el porcentaje de cambio
        if monto_ventas_ayer > 0:
            porcentaje_incremento = ((monto_ventas_dia - monto_ventas_ayer) / monto_ventas_ayer) * 100
        else:
            porcentaje_incremento = 0  # Si no hay ventas ayer, no hay cambio

            # Imprimir el porcentaje de incremento para depuración
            print(f"El valor del porcentaje_incremento es: {porcentaje_incremento}")

        # Determinar la dirección de la flecha
        if porcentaje_incremento > 0:
            direccion_flecha = 'up'  # Flecha hacia arriba si hubo incremento
        elif porcentaje_incremento < 0:
            direccion_flecha = 'down'  # Flecha hacia abajo si hubo decremento
        else:
            direccion_flecha = 'none'  # Si no hubo cambio


        # Obtener las ventas anuales
        ventas_anio = Venta.objects.filter(fecha_venta__year=now.year).values('fecha_venta__month').annotate(ventas_mes=Sum('total')).order_by('fecha_venta__month')
        
        # Crear las etiquetas para cada mes (Enero, Febrero, etc.)
        ventas_labels_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Recoger los datos de ventas mensuales (puedes agregar más lógica si lo deseas)
        ventas_data_meses = [0] * 12  # Iniciar lista con 12 valores en 0 (uno por cada mes)
        
        for venta in ventas_anio:
            ventas_data_meses[venta['fecha_venta__month'] - 1] = float(venta['ventas_mes'] or 0)  # Asignamos el total de cada mes

        # Obtener datos reales del inventario
        productos = Product.objects.all()
        productos_stock_bajo = [p for p in productos if p.get_stock_actual() < p.stock_minimo]
        
        # Obtener últimos cambios de stock
        ultimos_cambios_stock = StockVariable.objects.select_related(
            'producto'
        ).order_by('-id')[:5]  # Usamos id para ordenar por más reciente
        
        # Obtener el detalle de todas las ventas, agrupado por producto y sumando las cantidades
        detalle_ventas = DetalleVenta.objects.values('producto__name').annotate(
            total_cantidad=Sum('cantidad')
        )


        # Preparar los datos para el gráfico de productos vendidos
        nombres_productos = [detalle['producto__name'] for detalle in detalle_ventas]
        cantidad_productos = [detalle['total_cantidad'] for detalle in detalle_ventas]

        # Si no hay productos vendidos, asignar valores predeterminados
        if not nombres_productos:
            nombres_productos = ['Sin productos vendidos']
            cantidad_productos = [0]


        #print(nombres_productos)
        #print(cantidad_productos)
        #print(ventas_labels_meses)
        #print(ventas_data_meses)

        # Datos para el dashboard
        context.update({
            'monto_ventas_dia': monto_ventas_dia,
            'porcentaje_incremento': round(porcentaje_incremento, 2),  # Redondear el porcentaje a 2 decimales
            'direccion_flecha': direccion_flecha,
            'ventas_labels_meses': ventas_labels_meses,
            'ventas_data_meses': ventas_data_meses,
            'nombres_productos' : nombres_productos,
            'cantidad_productos' : cantidad_productos,
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
            'labels_nombre_productos': [p.name for p in productos[:5]],
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