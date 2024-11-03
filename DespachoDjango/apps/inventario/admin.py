from django.contrib import admin
from .models import Product, StockVariable, DetalleCompra, OrdenDespacho, SeguimientoEnvio, ReporteEnvios, ReporteFinanciero

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)

@admin.register(StockVariable)
class StockVariableAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_stock', 'fecha_actualizacion')

@admin.register(OrdenDespacho)
class OrdenDespachoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'transportista', 'fecha_creacion')

@admin.register(SeguimientoEnvio)
class SeguimientoEnvioAdmin(admin.ModelAdmin):
    list_display = ('orden', 'estado_envio', 'fecha_actualizacion')

admin.site.register(DetalleCompra)
admin.site.register(ReporteEnvios)
admin.site.register(ReporteFinanciero)
