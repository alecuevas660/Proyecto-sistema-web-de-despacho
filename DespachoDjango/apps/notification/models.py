from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Product, DetalleVenta, OrdenDespacho

class Notification(models.Model):
    """Modelo para registrar notificaciones del sistema."""
    mensaje = models.TextField('Mensaje de Notificación')
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    leido = models.BooleanField('Leído', default=False)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Notificación: {self.mensaje[:50]}..."

# Función de verificación de stock bajo
def verificar_stock(producto):
    estado, nivel = producto.get_stock_status()
    if nivel in ('warning', 'danger'):
        mensaje = f"El producto '{producto.name}' tiene stock {estado}."
        Notification.objects.create(mensaje=mensaje)

# Señal para notificación de bajo stock al actualizar detalle de venta
@receiver(post_save, sender=DetalleVenta)
def notificar_bajo_stock(sender, instance, **kwargs):
    verificar_stock(instance.producto)

# Señal para notificación de nueva orden de despacho
@receiver(post_save, sender=OrdenDespacho)
def notificar_nueva_orden(sender, instance, created, **kwargs):
    if created:
        mensaje = f"Se ha creado una nueva orden de despacho para el cliente {instance.cliente.get_full_name()}."
        Notification.objects.create(mensaje=mensaje)
