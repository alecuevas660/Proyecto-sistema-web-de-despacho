from django.contrib import admin
from .models import (
    Product, 
    StockVariable, 
    DetalleCompra, 
    OrdenDespacho, 
    SeguimientoEnvio, 
    ReporteEnvios, 
    ReporteFinanciero, 
    Categoria,
    Despacho,
    DetalleDespacho
)

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

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'created_at')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activo',)

class DetalleDespachoInline(admin.TabularInline):
    model = DetalleDespacho
    extra = 1
    raw_id_fields = ('producto',)
    autocomplete_fields = ['producto']
    fields = ['producto', 'cantidad', 'precio_unitario']
    readonly_fields = []

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        form.base_fields['producto'].queryset = Product.objects.filter(activo=True)
        return formset

@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
    list_display = ['numero_despacho', 'cliente', 'estado', 'fecha_creacion', 'total', 'direccion_entrega']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['numero_despacho', 'cliente__username', 'cliente__first_name', 'cliente__last_name', 'direccion_entrega']
    readonly_fields = ['numero_despacho', 'fecha_creacion', 'total']
    inlines = [DetalleDespachoInline]
    fieldsets = (
        ('Información Principal', {
            'fields': ('numero_despacho', 'cliente', 'estado')
        }),
        ('Detalles de Entrega', {
            'fields': ('direccion_entrega', 'observaciones')
        }),
        ('Información Adicional', {
            'fields': ('fecha_creacion', 'total'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si es una edición
            return self.readonly_fields + ['cliente']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.save()
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.precio_unitario and instance.producto:
                instance.precio_unitario = instance.producto.price
            instance.save()
        formset.save_m2m()
        form.instance.actualizar_total()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'transport':
            return qs.filter(estado__in=['pendiente', 'confirmada'])
        return qs.filter(cliente=request.user)

admin.site.register(DetalleCompra)
admin.site.register(ReporteEnvios)
admin.site.register(ReporteFinanciero)