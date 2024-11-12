import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

class EstadoEnvio:
    """Opciones para el estado de envío"""
    PENDIENTE = 'pendiente'
    EN_TRANSITO = 'en_transito'
    ENTREGADO = 'entregado'
    CANCELADO = 'cancelado'

    CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (EN_TRANSITO, 'En Tránsito'),
        (ENTREGADO, 'Entregado'),
        (CANCELADO, 'Cancelado'),
    ]

class Categoria(models.Model):
    """Modelo que representa una categoría de producto."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField('Nombre', max_length=100, unique=True)
    descripcion = models.TextField('Descripción', blank=True)
    activo = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Actualización', auto_now=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Product(models.Model):
    """Modelo que representa un producto en el sistema."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        'Nombre',
        max_length=255,
        validators=[MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')]
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,  # PROTECT evita eliminar categorías con productos
        related_name='productos',
        verbose_name='Categoría'
    )
    description = models.TextField('Descripción', null=True, blank=True)
    price = models.DecimalField(
        'Precio',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock_minimo = models.PositiveIntegerField('Stock Mínimo', default=0)
    activo = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Actualización', auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
        unique_together = ['name', 'categoria']

    def __str__(self):
        return self.name

    def get_stock_actual(self):
        """Retorna el stock actual del producto"""
        return self.stock_variables.latest('fecha_actualizacion').cantidad_stock if self.stock_variables.exists() else 0

    def get_stock_status(self):
        """Retorna el estado del stock basado en el stock actual y mínimo"""
        stock_actual = self.get_stock_actual()
        if stock_actual >= self.stock_minimo * 3/3:  # 100% o más del mínimo
            return ('Óptimo', 'success')
        elif stock_actual >= self.stock_minimo * 2/3:  # 66% o más del mínimo
            return ('Bajo', 'warning')
        else:  # Menos del 66% del mínimo
            return ('Crítico', 'danger')

    def clean(self):
        """Validaciones personalizadas del modelo"""
        if self.price and self.price <= 0:
            raise ValidationError({'price': 'El precio debe ser mayor que 0'})
        
        if self.stock_minimo and self.stock_minimo < 0:
            raise ValidationError({'stock_minimo': 'El stock mínimo no puede ser negativo'})
        
        if self.name and self.categoria:
            exists = Product.objects.filter(
                name__iexact=self.name,
                categoria=self.categoria
            ).exclude(pk=self.pk).exists()
            
            if exists:
                raise ValidationError({
                    'name': 'Ya existe un producto con este nombre en la misma categoría'
                })

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        self.full_clean()
        super().save(*args, **kwargs)

class StockVariable(models.Model):
    """Modelo que representa el historial de stock de un producto."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    producto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_variables',
        verbose_name='Producto'
    )
    cantidad_stock = models.PositiveIntegerField('Cantidad en Stock')
    fecha_actualizacion = models.DateTimeField('Fecha de Actualización', auto_now=True)
    motivo = models.CharField('Motivo de Actualización', max_length=255, blank=True)


    class Meta:
        db_table = 'stock_variable'
        verbose_name = 'Stock Variable'
        verbose_name_plural = 'Stock Variables'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f"{self.producto.name} - Stock: {self.cantidad_stock}"

class DetalleCompra(models.Model):
    """Modelo que representa los detalles de una compra."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    producto = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='detalles_compra',
        verbose_name='Producto'
    )
    cantidad_productos = models.PositiveIntegerField('Cantidad')
    precio_unitario = models.DecimalField(
        'Precio Unitario',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    fecha_compra = models.DateTimeField('Fecha de Compra', auto_now_add=True)

    class Meta:
        db_table = 'detalle_compra'
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compras'

    def __str__(self):
        return f"Compra de {self.cantidad_productos} {self.producto.name}"

    @property
    def total(self):
        """Calcula el total de la compra"""
        return self.cantidad_productos * self.precio_unitario

class OrdenDespacho(models.Model):
    """Modelo que representa una orden de despacho."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ordenes_despacho',
        limit_choices_to={'role': 'client'},
        verbose_name='Cliente'
    )
    transportista = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transportes',
        limit_choices_to={'role': 'transport'},
        verbose_name='Transportista'
    )
    compra = models.ForeignKey(
        DetalleCompra,
        on_delete=models.PROTECT,
        related_name='ordenes',
        verbose_name='Compra'
    )
    direccion_entrega = models.TextField('Dirección de Entrega')
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    observaciones = models.TextField('Observaciones', blank=True)

    class Meta:
        db_table = 'orden_despacho'
        verbose_name = 'Orden de Despacho'
        verbose_name_plural = 'Órdenes de Despacho'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Orden #{self.id} - Cliente: {self.cliente.get_full_name()}"

class SeguimientoEnvio(models.Model):
    """Modelo que representa el seguimiento de un envío."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orden = models.ForeignKey(
        OrdenDespacho,
        on_delete=models.CASCADE,
        related_name='seguimientos',
        verbose_name='Orden de Despacho'
    )
    estado_envio = models.CharField(
        'Estado',
        max_length=20,
        choices=EstadoEnvio.CHOICES,
        default=EstadoEnvio.PENDIENTE
    )
    ubicacion_actual = models.CharField('Ubicación Actual', max_length=255, blank=True)
    comentarios = models.TextField('Comentarios', blank=True)
    fecha_actualizacion = models.DateTimeField('Fecha de Actualización', auto_now=True)

    class Meta:
        db_table = 'seguimiento_envio'
        verbose_name = 'Seguimiento de Envío'
        verbose_name_plural = 'Seguimientos de Envíos'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f"Seguimiento de Orden #{self.orden.id} - {self.get_estado_envio_display()}"

class ReporteEnvios(models.Model):
    """Modelo que representa un reporte de envíos."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_inicio = models.DateField('Fecha Inicial')
    fecha_fin = models.DateField('Fecha Final')
    total_envios = models.PositiveIntegerField('Total de Envíos', default=0)
    envios_completados = models.PositiveIntegerField('Envíos Completados', default=0)
    envios_pendientes = models.PositiveIntegerField('Envíos Pendientes', default=0)
    fecha_generacion = models.DateTimeField('Fecha de Generación', auto_now_add=True)

    class Meta:
        db_table = 'reporte_envios'
        verbose_name = 'Reporte de Envíos'
        verbose_name_plural = 'Reportes de Envíos'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f"Reporte de Envíos {self.fecha_inicio} - {self.fecha_fin}"

class ReporteFinanciero(models.Model):
    """Modelo que representa un reporte financiero."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_inicio = models.DateField('Fecha Inicial')
    fecha_fin = models.DateField('Fecha Final')
    total_ventas = models.DecimalField(
        'Total Ventas',
        max_digits=12,
        decimal_places=2,
        default=0
    )
    total_envios = models.PositiveIntegerField('Total Envíos', default=0)
    fecha_generacion = models.DateTimeField('Fecha de Generación', auto_now_add=True)

    class Meta:
        db_table = 'reporte_financiero'
        verbose_name = 'Reporte Financiero'
        verbose_name_plural = 'Reportes Financieros'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f"Reporte Financiero {self.fecha_inicio} - {self.fecha_fin}"

class EstadoDespacho:
    PENDIENTE = 'pendiente'
    CONFIRMADO = 'confirmado'
    EN_PREPARACION = 'en_preparacion'
    EN_RUTA = 'en_ruta'
    ENTREGADO = 'entregado'
    CANCELADO = 'cancelado'

    CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
        (EN_PREPARACION, 'En Preparación'),
        (EN_RUTA, 'En Ruta'),
        (ENTREGADO, 'Entregado'),
        (CANCELADO, 'Cancelado'),
    ]

class Despacho(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_despacho = models.CharField(max_length=10, unique=True, editable=False)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='despachos'
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoDespacho.CHOICES,
        default=EstadoDespacho.PENDIENTE
    )
    direccion_entrega = models.TextField()
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Despacho #{self.numero_despacho}"

    def save(self, *args, **kwargs):
        if not self.numero_despacho:
            last_despacho = Despacho.objects.order_by('-numero_despacho').first()
            if last_despacho:
                last_number = int(last_despacho.numero_despacho[3:])
                self.numero_despacho = f'DS-{str(last_number + 1).zfill(6)}'
            else:
                self.numero_despacho = 'DS-000001'
        super().save(*args, **kwargs)

    def actualizar_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()

class DetalleDespacho(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    despacho = models.ForeignKey(
        Despacho,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='detalles_despacho'
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )

    @property
    def subtotal(self):
        if self.cantidad is None or self.precio_unitario is None:
            return 0
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        if not self.precio_unitario and self.producto:
            self.precio_unitario = self.producto.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.name if self.producto else 'Sin producto'} - {self.cantidad} unidades"

    class Meta:
        verbose_name = 'Detalle de Despacho'
        verbose_name_plural = 'Detalles de Despacho'
