import uuid
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from apps.inventario.models import Product

# clase venta
class Venta(models.Model):
    """Modelo que representa una venta en el sistema."""

    class MetodoPago(models.TextChoices):
        EFECTIVO = 'efectivo', 'Efectivo'
        TARJETA = 'tarjeta', 'Tarjeta'
        TRANSFERENCIA = 'transferencia', 'Transferencia'
        OTRO = 'otro', 'Otro'

    # Campos de identificación
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_venta = models.CharField(
        'Número de Venta',
        max_length=10,
        unique=True,
        editable=False
    )

    # Campos de cliente
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='compras',
        limit_choices_to={'role': 'client'},
        verbose_name='Cliente',
        null=True,
        blank=True
    )
    rut_cliente = models.CharField(
        'RUT Cliente',
        max_length=12,
        blank=True
    )

    # Campos de pago
    metodo_pago = models.CharField(
        'Método de Pago',
        max_length=20,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO
    )
    subtotal = models.DecimalField(
        'Subtotal',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    impuestos = models.DecimalField(
        'Impuestos',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total = models.DecimalField(
        'Total',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    # Campos de estado y seguimiento
    estado = models.CharField(
        'Estado',
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('completada', 'Completada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendiente'
    )
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ventas_realizadas',
        limit_choices_to={'is_staff': True},
        verbose_name='Vendedor'
    )
    notas = models.TextField('Notas', blank=True)

    # Campos de fecha
    fecha_venta = models.DateTimeField('Fecha de Venta', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Última Actualización', auto_now=True)

    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha_venta']

    def __str__(self):
        return f'Venta {self.numero_venta} - {self.cliente.get_full_name()}'

    def save(self, *args, **kwargs):
        """Genera número de venta y calcula totales antes de guardar."""
        if not self.numero_venta:
            last_venta = Venta.objects.order_by('-numero_venta').first()
            if last_venta:
                last_number = int(last_venta.numero_venta[1:])
                self.numero_venta = f'V{str(last_number + 1).zfill(6)}'
            else:
                self.numero_venta = 'V000001'

        self.subtotal = sum(detalle.subtotal for detalle in self.detalles.all())
        self.impuestos = self.subtotal * Decimal('0.19')  # 19% IVA
        self.total = self.subtotal + self.impuestos

        super().save(*args, **kwargs)



# Modelo de detalle de venta
class DetalleVenta(models.Model):
    """Modelo que representa el detalle de una venta."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venta = models.ForeignKey(
        Venta,
        related_name='detalles',
        on_delete=models.CASCADE,
        verbose_name='Venta'
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='ventas',
        verbose_name='Producto'
    )
    cantidad = models.PositiveIntegerField(
        'Cantidad',
        validators=[MinValueValidator(1)]
    )
    precio_unitario = models.DecimalField(
        'Precio Unitario',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        default=0.00
    )
    descuento = models.DecimalField(
        'Descuento',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    subtotal = models.DecimalField(
        'Subtotal',
        max_digits=10,
        decimal_places=2,
        editable=False,
        default=0.00
    )

    class Meta:
        db_table = 'detalles_venta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'
        unique_together = [['venta', 'producto']]

    def __str__(self):
        return f'{self.cantidad} x {self.producto.name}'

    def save(self, *args, **kwargs):
        """Calcula el subtotal antes de guardar."""
        self.precio_unitario = self.precio_unitario or self.producto.price
        self.subtotal = (self.cantidad * self.precio_unitario) - self.descuento

        # Actualizar stock
        if not self.pk:  # Si es una nueva venta
            stock = self.producto.stock_variables.latest('fecha_actualizacion')
            if stock.cantidad_stock < self.cantidad:
                raise ValueError('No hay suficiente stock disponible')
            stock.cantidad_stock -= self.cantidad
            stock.save()

        super().save(*args, **kwargs)

        # Actualizar totales de la venta
        self.venta.save()

    def delete(self, *args, **kwargs):
        """Restaura el stock al eliminar un detalle de venta."""
        stock = self.producto.stock_variables.latest('fecha_actualizacion')
        stock.cantidad_stock += self.cantidad
        stock.save()
        super().delete(*args, **kwargs)
        self.venta.save()

