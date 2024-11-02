"""
Este módulo define los modelos de datos para el sistema de gestión de ventas, 
incluyendo Venta y DetalleVenta.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator
from apps.inventario.models import Product

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
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
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
