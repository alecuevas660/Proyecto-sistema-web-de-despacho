import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Product

class StockAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "stock_alerts",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "stock_alerts",
            self.channel_name
        )

    async def stock_alert(self, event):
        # Enviar alerta al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'stock_alert',
            'product': event['product'],
            'current_stock': event['current_stock'],
            'min_stock': event['min_stock'],
            'message': event['message']
        }))
