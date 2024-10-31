from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Venta(models.Model):
    METODOS_PAGO = (
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    )
    
    nombre_cliente = models.CharField(max_length=200)
    rut_cliente = models.CharField(max_length=12, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey('users.User', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        
    def __str__(self):
        return f'Venta {self.id} - {self.nombre_cliente}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('inventario.Producto', on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'
        
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio
        super().save(*args, **kwargs)
