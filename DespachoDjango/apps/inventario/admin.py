from django.contrib import admin
from .models import Product, StockVariable

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
