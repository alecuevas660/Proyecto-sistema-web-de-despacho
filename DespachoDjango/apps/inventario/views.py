from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Q, F
from .models import Product, StockVariable, Categoria
from django.contrib import messages
from .forms import ProductForm, StockUpdateForm
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from openpyxl import Workbook
from datetime import datetime

# Create your views here.

class InventarioListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventario/inventario_list.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todos los productos con su último stock
        productos = Product.objects.all()
        productos_atencion = []
        total_stock_bajo = 0

        # Filtrar productos que requieren atención (stock bajo o crítico)
        for producto in productos:
            stock_actual = producto.get_stock_actual()
            if stock_actual < producto.stock_minimo:  # Si está por debajo del mínimo
                productos_atencion.append(producto)
                total_stock_bajo += 1

        context['productos_stock_bajo'] = productos_atencion
        context['total_productos'] = productos.count()
        context['total_stock_bajo'] = total_stock_bajo
        
        return context

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventario/product_list.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filtro de categoría
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        # Filtro de stock
        stock_filter = self.request.GET.get('stock')
        if stock_filter == 'optimo':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__gte=F('stock_minimo')
            )
        elif stock_filter == 'bajo':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__lt=F('stock_minimo'),
                stock_variables__cantidad_stock__gte=F('stock_minimo') * 2/3
            )
        elif stock_filter == 'critico':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__lt=F('stock_minimo') * 2/3
            )

        # Búsqueda
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search': self.request.GET.get('search', ''),
            'stock_filter': self.request.GET.get('stock', ''),
            'categoria_filter': self.request.GET.get('categoria', ''),
            'categorias': Categoria.objects.filter(activo=True),
        })
        return context

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventario/product_form.html'
    success_url = reverse_lazy('inventario:product_list')
    permission_required = 'inventario.add_product'

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, error)
                else:
                    messages.error(self.request, f"{form[field].label}: {error}")
        return super().form_invalid(form)

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            
            # Validaciones adicionales de negocio
            if self.object.price > 1000000:
                messages.warning(self.request, 'Has establecido un precio muy alto. Por favor, verifica que sea correcto.')
            
            if self.object.stock_minimo > 100:
                messages.warning(self.request, 'Has establecido un stock mínimo alto. Esto podría generar muchas alertas.')

            response = super().form_valid(form)
            
            # Crear registro inicial de stock
            StockVariable.objects.create(
                producto=self.object,
                cantidad_stock=0,
                motivo='Registro inicial'
            )
            
            messages.success(
                self.request, 
                f'Producto "{self.object.name}" creado exitosamente en la categoría {self.object.categoria.nombre}.'
            )
            return response
            
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(self.request, f"{error}")
            return self.form_invalid(form)
        except Exception as e:
            messages.error(
                self.request, 
                f'Error inesperado al crear el producto: {str(e)}'
            )
            return self.form_invalid(form)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventario/product_form.html'
    success_url = reverse_lazy('inventario:product_list')
    permission_required = 'inventario.change_product'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return response

@method_decorator(require_POST, name='delete')
class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'inventario.delete_product'
    success_url = reverse_lazy('inventario:product_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(request, 'Producto eliminado exitosamente.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return HttpResponseRedirect(success_url)
        except Exception as e:
            messages.error(request, 'No se pudo eliminar el producto.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False}, status=400)
            return HttpResponseRedirect(success_url)

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'inventario/category_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

    def get_queryset(self):
        queryset = Categoria.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(descripcion__icontains=search_query)
            )
        return queryset

class CategoriaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Categoria
    template_name = 'inventario/category_form.html'
    fields = ['nombre', 'descripcion', 'activo']
    success_url = reverse_lazy('inventario:category_list')
    permission_required = 'inventario.add_categoria'

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente.')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Categoria
    template_name = 'inventario/category_form.html'
    fields = ['nombre', 'descripcion', 'activo']
    success_url = reverse_lazy('inventario:category_list')
    permission_required = 'inventario.change_categoria'

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada exitosamente.')
        return super().form_valid(form)

class StockUpdateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = StockVariable
    form_class = StockUpdateForm
    template_name = 'inventario/stock_form.html'
    permission_required = 'inventario.add_stockvariable'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = Product.objects.get(pk=self.kwargs['pk'])
        context['producto'] = producto
        context['stock_actual'] = producto.get_stock_actual()
        return context

    def form_valid(self, form):
        try:
            form.instance.producto_id = self.kwargs['pk']
            producto = Product.objects.get(pk=self.kwargs['pk'])
            nueva_cantidad = form.cleaned_data['cantidad_stock']
            
            # Validaciones de negocio para el stock
            if nueva_cantidad == 0:
                messages.warning(self.request, 'Has establecido el stock en 0.')
            
            if nueva_cantidad < producto.stock_minimo:
                messages.warning(
                    self.request, 
                    f'El nuevo stock ({nueva_cantidad}) está por debajo del mínimo requerido ({producto.stock_minimo}).'
                )
            
            if not form.instance.motivo.strip():
                form.add_error('motivo', 'Debe proporcionar un motivo para la actualización')
                return self.form_invalid(form)

            response = super().form_valid(form)
            messages.success(
                self.request, 
                f'Stock actualizado exitosamente. Nuevo stock: {nueva_cantidad} unidades.'
            )
            return response
            
        except ValidationError as e:
            messages.error(self.request, 'Error al actualizar el stock:')
            for error in e.messages:
                messages.error(self.request, error)
            return self.form_invalid(form)
        except Product.DoesNotExist:
            messages.error(self.request, 'El producto no existe.')
            return redirect('inventario:inventario_list')
        except Exception as e:
            messages.error(
                self.request, 
                f'Error inesperado al actualizar el stock: {str(e)}'
            )
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('inventario:inventario_list')

def exportar_inventario(request):
    wb = Workbook()
    
    # 1. Hoja de Resumen General
    ws_resumen = wb.active
    ws_resumen.title = "Resumen General"
    
    # Encabezado con fecha del reporte
    ws_resumen.append(['REPORTE DE INVENTARIO'])
    ws_resumen.append(['Fecha de generación:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    ws_resumen.append([])  # Línea en blanco

    # Estadísticas generales
    total_productos = Product.objects.count()
    total_categorias = Categoria.objects.filter(activo=True).count()
    
    # Modificamos la consulta para usar el último stock registrado
    productos_stock_bajo = sum(1 for producto in Product.objects.all() 
                             if producto.get_stock_actual() < producto.stock_minimo)
    
    # Calculamos el valor total usando el stock actual
    valor_total_inventario = sum(
        producto.get_stock_actual() * producto.price 
        for producto in Product.objects.all()
    )

    estadisticas = [
        ['Total de Productos:', total_productos],
        ['Categorías Activas:', total_categorias],
        ['Productos con Stock Bajo:', productos_stock_bajo],
        ['Valor Total del Inventario:', f"${valor_total_inventario:,.2f}"],
        []  # Línea en blanco
    ]
    for stat in estadisticas:
        ws_resumen.append(stat)

    # 2. Hoja de Inventario Detallado
    ws_inventario = wb.create_sheet("Inventario Detallado")
    headers_inventario = [
        'Código', 
        'Nombre', 
        'Categoría',
        'Stock Actual',
        'Stock Mínimo',
        'Estado Stock',
        'Precio Unitario',
        'Valor Total',
        'Última Actualización',
        'Ubicación',
        'Notas'
    ]
    ws_inventario.append(headers_inventario)

    productos = Product.objects.all().select_related('categoria')
    for producto in productos:
        stock_actual = producto.get_stock_actual()
        estado_stock = 'ÓPTIMO'
        if stock_actual < producto.stock_minimo:
            estado_stock = 'CRÍTICO'
        elif stock_actual < (producto.stock_minimo * 1.5):
            estado_stock = 'BAJO'

        ultima_actualizacion = producto.stock_variables.order_by('-created_at').first()

        ws_inventario.append([
            producto.codigo if hasattr(producto, 'codigo') else 'N/A',
            producto.name,
            producto.categoria.nombre if producto.categoria else 'Sin categoría',
            stock_actual,
            producto.stock_minimo,
            estado_stock,
            producto.price,
            stock_actual * producto.price,
            ultima_actualizacion.created_at.strftime('%Y-%m-%d %H:%M:%S') if ultima_actualizacion else 'N/A',
            producto.ubicacion if hasattr(producto, 'ubicacion') else 'N/A',
            producto.description or ''
        ])

    # 3. Hoja de Productos Críticos
    ws_criticos = wb.create_sheet("Productos Críticos")
    headers_criticos = [
        'Código',
        'Nombre',
        'Stock Actual',
        'Stock Mínimo',
        'Diferencia',
        'Días sin Reposición',
        'Precio Unitario',
        'Valor a Reponer'
    ]
    ws_criticos.append(headers_criticos)

    # Filtramos productos críticos usando get_stock_actual()
    productos_criticos = [p for p in Product.objects.all() 
                         if p.get_stock_actual() < p.stock_minimo]
    
    for producto in productos_criticos:
        stock_actual = producto.get_stock_actual()
        diferencia = producto.stock_minimo - stock_actual
        ultima_actualizacion = producto.stock_variables.order_by('-created_at').first()
        dias_sin_reposicion = (datetime.now().date() - ultima_actualizacion.created_at.date()).days if ultima_actualizacion else 0
        
        ws_criticos.append([
            producto.codigo if hasattr(producto, 'codigo') else 'N/A',
            producto.name,
            stock_actual,
            producto.stock_minimo,
            diferencia,
            dias_sin_reposicion,
            producto.price,
            diferencia * producto.price
        ])

    # 4. Hoja de Análisis por Categoría
    ws_categorias = wb.create_sheet("Análisis por Categoría")
    headers_categorias = [
        'Categoría',
        'Total Productos',
        'Productos Stock Bajo',
        'Valor Total Inventario',
        'Valor Promedio por Producto'
    ]
    ws_categorias.append(headers_categorias)

    categorias = Categoria.objects.filter(activo=True)
    for categoria in categorias:
        productos_cat = Product.objects.filter(categoria=categoria)
        total_productos_cat = productos_cat.count()
        
        # Calculamos productos con stock bajo
        productos_bajos_cat = sum(1 for p in productos_cat 
                                if p.get_stock_actual() < p.stock_minimo)
        
        # Calculamos valor total del inventario para la categoría
        valor_total_cat = sum(p.get_stock_actual() * p.price for p in productos_cat)
        valor_promedio = valor_total_cat / total_productos_cat if total_productos_cat > 0 else 0

        ws_categorias.append([
            categoria.nombre,
            total_productos_cat,
            productos_bajos_cat,
            valor_total_cat,
            valor_promedio
        ])

    # Aplicar formato a todas las hojas
    for ws in wb.worksheets:
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width

    # Crear la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Reporte_Inventario_Completo_{}.xlsx'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )

    wb.save(response)
    return response
