"""
Este módulo define los modelos de datos para el sistema de gestión de productos, 
incluyendo Product, StockVariable, DetalleCompra, OrdenDespacho, SeguimientoEnvio, 
ReporteEnvios y ReporteFinanciero.
"""

import uuid
from django.db import models

# Modelo de producto
class Product(models.Model):
    """
    Modelo que representa un producto en el sistema.
    
    Attributes:
        id (UUIDField): Identificador único del producto.
        name (CharField): Nombre del producto.
        description (TextField): Descripción del producto.
        price (DecimalField): Precio del producto.
        created_at (DateTimeField): Fecha y hora de creación del producto.
        updated_at (DateTimeField): Fecha y hora de la última actualización del producto.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Devuelve el nombre del producto como representación en cadena."""
        return str(self.name) if self.name else "Nombre no disponible"

    class Meta:
        """
        Configuración de la tabla para el modelo Product.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
            ordering (list): Orden predeterminado para las consultas.
        """
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']


# Modelo de stock variable
class StockVariable(models.Model):
    """
    Modelo que representa la cantidad de stock de un producto.
    
    Attributes:
        id (UUIDField): Identificador único del stock variable.
        id_producto (ForeignKey): Relación con el modelo Product.
        cantidad_stock (IntegerField): Cantidad de stock disponible.
        fecha_actualizacion (DateTimeField): 
        Fecha y hora de la última actualización del stock.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_producto = models.ForeignKey(Product, on_delete=models.CASCADE,
                                    related_name='stock_variables')
    """Linea de arriba muy larga y se decidió acortar"""
    cantidad_stock = models.IntegerField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Configuración de la tabla para el modelo StockVariable.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'stock_variable'
        verbose_name = 'Stock Variable'
        verbose_name_plural = 'Stock Variables'


# Modelo de detalle de compra
class DetalleCompra(models.Model):
    """
    Modelo que representa los detalles de una compra.
    
    Attributes:
        id (UUIDField): Identificador único del detalle de compra.
        fecha_compra (DateTimeField): Fecha y hora de la compra.
        cantidad_productos (IntegerField): Cantidad de productos comprados.
        id_producto (ForeignKey): Relación con el modelo Product.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    cantidad_productos = models.IntegerField()
    id_producto = models.ForeignKey(Product, on_delete=models.CASCADE,
                                    related_name='detalles_compra')
    """Linea de arriba muy larga y se decidió acortar"""

    class Meta:
        """
        Configuración de la tabla para el modelo DetalleCompra.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'detalle_compra'
        verbose_name = 'Detalle Compra'
        verbose_name_plural = 'Detalles Compra'


# Modelo de orden de despacho
class OrdenDespacho(models.Model):
    """
    Modelo que representa una orden de despacho.
    
    Attributes:
        id (UUIDField): Identificador único de la orden de despacho.
        id_cliente (ForeignKey): Relación con el modelo Cliente.
        id_tran (ForeignKey): Relación con el modelo Transportista.
        id_compra (ForeignKey): Relación con el modelo DetalleCompra.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey('useraccount.Cliente', on_delete=models.CASCADE)
    id_tran = models.ForeignKey('useraccount.Transportista', on_delete=models.CASCADE)
    id_compra = models.ForeignKey(DetalleCompra, on_delete=models.CASCADE)

    class Meta:
        """
        Configuración de la tabla para el modelo OrdenDespacho.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'orden_despacho'
        verbose_name = 'Orden de Despacho'
        verbose_name_plural = 'Órdenes de Despacho'


# Modelo de seguimiento de envío
class SeguimientoEnvio(models.Model):
    """
    Modelo que representa el seguimiento de un envío.
    
    Attributes:
        id (UUIDField): Identificador único del seguimiento de envío.
        estado_envio (CharField): Estado actual del envío.
        id_cliente (ForeignKey): Relación con el modelo Cliente.
        id_orden (ForeignKey): Relación con el modelo OrdenDespacho.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estado_envio = models.CharField(max_length=100)
    id_cliente = models.ForeignKey('useraccount.Cliente', on_delete=models.CASCADE)
    id_orden = models.ForeignKey(OrdenDespacho, on_delete=models.CASCADE)

    class Meta:
        """
        Configuración de la tabla para el modelo SeguimientoEnvio.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'seguimiento_envio'
        verbose_name = 'Seguimiento de Envío'
        verbose_name_plural = 'Seguimientos de Envíos'


# Modelos de reporte
class ReporteEnvios(models.Model):
    """
    Modelo que representa un reporte de envíos.
    
    Attributes:
        id (UUIDField): Identificador único del reporte de envíos.
        id_cliente (ForeignKey): Relación con el modelo Cliente.
        cantidad_envios (IntegerField): Cantidad de envíos realizados.
        fecha_reporte (DateField): Fecha del reporte.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey('useraccount.Cliente', on_delete=models.CASCADE)
    cantidad_envios = models.IntegerField()
    fecha_reporte = models.DateField()

    class Meta:
        """
        Configuración de la tabla para el modelo ReporteEnvios.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'reporte_envios'
        verbose_name = 'Reporte de Envío'
        verbose_name_plural = 'Reportes de Envíos'


class ReporteFinanciero(models.Model):
    """
    Modelo que representa un reporte financiero de ventas.
    
    Attributes:
        id (UUIDField): Identificador único del reporte financiero.
        categoria_producto (CharField): Categoría del producto vendido.
        cantidad_vendida (IntegerField): Cantidad de productos vendidos.
        fecha_reporte (DateField): Fecha del reporte.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categoria_producto = models.CharField(max_length=100)
    cantidad_vendida = models.IntegerField()
    fecha_reporte = models.DateField()

    class Meta:
        """
        Configuración de la tabla para el modelo ReporteFinanciero.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'reporte_financiero'
        verbose_name = 'Reporte Financiero'
        verbose_name_plural = 'Reportes Financieros'
