from django.db import models
from django.conf import settings
import uuid

class EstadoOrden:
    PENDIENTE = 'pendiente'
    CONFIRMADA = 'confirmada'
    EN_PREPARACION = 'en_preparacion'
    EN_RUTA = 'en_ruta'
    ENTREGADA = 'entregada'
    CANCELADA = 'cancelada'

    CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADA, 'Confirmada'),
        (EN_PREPARACION, 'En Preparación'),
        (EN_RUTA, 'En Ruta'),
        (ENTREGADA, 'Entregada'),
        (CANCELADA, 'Cancelada'),
    ]

class OrdenDespacho(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_orden = models.CharField(max_length=10, unique=True, editable=False)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ordenes_cliente'
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoOrden.CHOICES,
        default=EstadoOrden.PENDIENTE
    )
    direccion_entrega = models.TextField()
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        app_label = 'ordenes'
        verbose_name = 'Orden de Despacho'
        verbose_name_plural = 'Órdenes de Despacho'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Orden #{self.numero_orden}"

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            last_order = OrdenDespacho.objects.order_by('-numero_orden').first()
            if last_order:
                last_number = int(last_order.numero_orden[3:])
                self.numero_orden = f'OD-{str(last_number + 1).zfill(6)}'
            else:
                self.numero_orden = 'OD-000001'
        super().save(*args, **kwargs)

    def actualizar_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()

class DetalleOrden(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orden = models.ForeignKey(
        OrdenDespacho,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        'inventario.Product',
        on_delete=models.PROTECT,
        related_name='detalles_orden'
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'ordenes'
        verbose_name = 'Detalle de Orden'
        verbose_name_plural = 'Detalles de Órdenes'

    def __str__(self):
        return f"{self.producto.name} - {self.cantidad} unidades"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario 