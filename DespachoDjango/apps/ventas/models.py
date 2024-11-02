"""
Este módulo define los modelos de datos para el sistema de gestión de ventas, 
incluyendo Venta y DetalleVenta.
"""

import uuid
from django.db import models

# Modelo de venta
class Venta(models.Model):
    """
    Modelo que representa una venta.
    
    Attributes:
        id (UUIDField): Identificador único de la venta.
        id_cliente (ForeignKey): Relación con el modelo Cliente.
        fecha_venta (DateTimeField): Fecha y hora de la venta.
        total_venta (DecimalField): Total de la venta.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey('useraccount.Cliente', on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """
        Configuración de la tabla para el modelo Venta.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'


# Modelo de detalle de venta
class DetalleVenta(models.Model):
    """
    Modelo que representa los detalles de una venta.
    
    Attributes:
        id (UUIDField): Identificador único del detalle de venta.
        cantidad_productos (IntegerField): Cantidad de productos vendidos.
        id_producto (ForeignKey): Relación con el modelo Product.
        id_venta (ForeignKey): Relación con el modelo Venta.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad_productos = models.IntegerField()
    id_producto = models.ForeignKey('inventario.Product',
                                    on_delete=models.CASCADE, related_name='detalles_venta')
    """Linea de arriba muy larga y se decidió acortar"""
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles_venta')

    class Meta:
        """
        Configuración de la tabla para el modelo DetalleVenta.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'detalle_venta'
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalles Venta'
