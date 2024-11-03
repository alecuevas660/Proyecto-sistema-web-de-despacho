from django.contrib import admin

from .models import Product, StockVariable, DetalleCompra, OrdenDespacho, SeguimientoEnvio, ReporteEnvios, ReporteFinanciero, Categoria

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_stock_actual', 'stock_minimo', 'activo')
    list_filter = ('activo',)
    search_fields = ('name', 'description')

@admin.register(StockVariable)
class StockVariableAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_stock', 'fecha_actualizacion', 'motivo')
    list_filter = ('producto',)
    search_fields = ('producto__name', 'motivo')
    
@admin.register(OrdenDespacho)
class OrdenDespachoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'transportista', 'fecha_creacion')

@admin.register(SeguimientoEnvio)
class SeguimientoEnvioAdmin(admin.ModelAdmin):
    list_display = ('orden', 'estado_envio', 'fecha_actualizacion')

admin.site.register(DetalleCompra)
admin.site.register(ReporteEnvios)
admin.site.register(ReporteFinanciero)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'created_at')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activo',)