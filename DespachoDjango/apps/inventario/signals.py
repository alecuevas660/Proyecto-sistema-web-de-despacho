from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import StockVariable

@receiver(post_save, sender=StockVariable)
def stock_update_handler(sender, instance, created, **kwargs):
    product = instance.producto
    if product.is_low_stock():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "stock_alerts",
            {
                "type": "stock_alert",
                "product": product.name,
                "current_stock": product.get_stock_actual(),
                "min_stock": product.stock_minimo,
                "message": f"¡Alerta! Stock bajo en {product.name}"
            }
        )
