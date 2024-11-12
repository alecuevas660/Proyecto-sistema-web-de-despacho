from django.contrib import admin
from apps.ordenes.models import OrdenDespacho, DetalleOrden

class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1
    readonly_fields = ['subtotal']

@admin.register(OrdenDespacho)
class OrdenDespachoAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'cliente', 'estado', 'fecha_creacion', 'total']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['numero_orden', 'cliente__username']
    inlines = [DetalleOrdenInline] 