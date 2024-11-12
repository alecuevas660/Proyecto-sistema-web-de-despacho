from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db import models, transaction
from django.db.models import Q, F
from django.forms import inlineformset_factory, forms
from .models import Product, StockVariable, Categoria, Despacho, DetalleDespacho, EstadoDespacho
from django.contrib import messages
from .forms import ProductForm, StockUpdateForm, ReporteInventarioForm
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from openpyxl import Workbook
from datetime import datetime, timedelta
from django.utils import timezone
from apps.users.models import User
from django import forms

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

def configurar_reporte(request):
    form = ReporteInventarioForm()
    return render(request, 'inventario/reporte_form.html', {'form': form})

def exportar_inventario(request):
    if request.method == 'GET':
        return configurar_reporte(request)
        
    form = ReporteInventarioForm(request.POST)
    if not form.is_valid():
        return render(request, 'inventario/reporte_form.html', {'form': form})
        
    # Obtener parámetros del formulario
    fecha_inicio = form.cleaned_data.get('fecha_inicio')
    fecha_fin = form.cleaned_data.get('fecha_fin')
    categorias = form.cleaned_data.get('categorias')
    umbral_stock_bajo = form.cleaned_data.get('umbral_stock_bajo')
    ordenar_por = form.cleaned_data.get('ordenar_por')
    incluir_inactivos = form.cleaned_data.get('incluir_inactivos')

    # Crear el libro de Excel
    wb = Workbook()
    ws_resumen = wb.active
    ws_resumen.title = "Resumen General"
    
    # Agregar parámetros del reporte
    ws_resumen.append(['REPORTE DE INVENTARIO'])
    ws_resumen.append(['Fecha de generación:', timezone.now().strftime('%Y-%m-%d %H:%M:%S')])
    ws_resumen.append(['Parámetros del reporte:'])
    ws_resumen.append(['Fecha inicio:', fecha_inicio or 'No especificada'])
    ws_resumen.append(['Fecha fin:', fecha_fin or 'No especificada'])
    ws_resumen.append(['Categorías:', ', '.join(c.nombre for c in categorias) if categorias else 'Todas'])
    ws_resumen.append(['Umbral stock bajo:', umbral_stock_bajo or 'Predeterminado'])
    ws_resumen.append([])

    # Filtrar productos según parámetros
    productos = Product.objects.all()
    
    if not incluir_inactivos:
        productos = productos.filter(activo=True)
    
    if categorias:
        productos = productos.filter(categoria__in=categorias)
        
    if fecha_inicio:
        productos = productos.filter(updated_at__gte=fecha_inicio)
        
    if fecha_fin:
        productos = productos.filter(updated_at__lte=fecha_fin)

    # Ordenar productos
    if ordenar_por == 'nombre':
        productos = productos.order_by('name')
    elif ordenar_por == 'categoria':
        productos = productos.order_by('categoria__nombre', 'name')
    elif ordenar_por == 'stock':
        productos = sorted(productos, key=lambda p: p.get_stock_actual())
    elif ordenar_por == 'precio':
        productos = productos.order_by('price')

    # ... (resto del código del reporte como estaba antes)
    
    # Modificar la lógica de stock bajo para usar el umbral personalizado
    if umbral_stock_bajo is not None:
        productos_stock_bajo = sum(1 for p in productos if p.get_stock_actual() < umbral_stock_bajo)
    else:
        productos_stock_bajo = sum(1 for p in productos if p.get_stock_actual() < p.stock_minimo)

    # ... (continuar con el resto del código del reporte)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Reporte_Inventario_Personalizado_{}.xlsx'.format(
        timezone.now().strftime('%Y%m%d_%H%M%S')
    )

    wb.save(response)
    return response

class DespachoListView(LoginRequiredMixin, ListView):
    model = Despacho
    template_name = 'inventario/despacho_list.html'
    context_object_name = 'despachos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'client':
            queryset = queryset.filter(cliente=self.request.user)
        
        # Búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(numero_despacho__icontains=search)
        
        return queryset.select_related('cliente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = EstadoDespacho.CHOICES
        return context

# Crear el FormSet para DetalleDespacho
DetalleDespachoFormSet = inlineformset_factory(
    Despacho,
    DetalleDespacho,
    fields=['producto', 'cantidad', 'precio_unitario'],
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    widgets={
        'producto': forms.Select(attrs={
            'class': 'form-control select2',
            'required': 'required'
        }),
        'cantidad': forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'required': 'required'
        }),
        'precio_unitario': forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    }
)

class DespachoCreateView(LoginRequiredMixin, CreateView):
    model = Despacho
    fields = ['direccion_entrega', 'observaciones']
    template_name = 'inventario/despacho_form.html'
    success_url = reverse_lazy('inventario:despacho_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = User.objects.filter(is_active=True)
        context['productos'] = Product.objects.filter(activo=True)
        context['estados'] = EstadoDespacho.CHOICES
        if self.request.POST:
            context['detalles'] = DetalleDespachoFormSet(
                self.request.POST,
                instance=self.object if self.object else None
            )
        else:
            context['detalles'] = DetalleDespachoFormSet(
                instance=self.object if self.object else None
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles']
        
        try:
            with transaction.atomic():
                # Primero guardamos el despacho
                self.object = form.save(commit=False)
                self.object.cliente = self.request.user
                self.object.save()

                # Ahora guardamos los detalles
                if detalles_formset.is_valid():
                    detalles = detalles_formset.save(commit=False)
                    for detalle in detalles:
                        detalle.despacho = self.object  # Asignamos el despacho al detalle
                        if not detalle.precio_unitario and detalle.producto:
                            detalle.precio_unitario = detalle.producto.price
                        detalle.save()
                    
                    # Eliminamos los detalles marcados para eliminar
                    for detalle in detalles_formset.deleted_objects:
                        detalle.delete()
                    
                    # Actualizamos el total
                    self.object.actualizar_total()
                else:
                    raise ValidationError('Error en los detalles del despacho')

                messages.success(self.request, 'Despacho creado exitosamente')
                return HttpResponseRedirect(self.get_success_url())
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear el despacho: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores en el formulario')
        return super().form_invalid(form)

class DespachoDetailView(LoginRequiredMixin, DetailView):
    model = Despacho
    template_name = 'inventario/despacho_detail.html'
    context_object_name = 'despacho'

class DespachoUpdateView(LoginRequiredMixin, UpdateView):
    model = Despacho
    fields = ['direccion_entrega', 'observaciones', 'estado']
    template_name = 'inventario/despacho_form.html'
    success_url = reverse_lazy('inventario:despacho_list')

    def form_valid(self, form):
        messages.success(self.request, 'Despacho actualizado exitosamente')
        return super().form_valid(form)

class DespachoEstadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Despacho
    fields = ['estado']
    template_name = 'inventario/despacho_estado_form.html'
    success_url = reverse_lazy('inventario:despacho_list')

    def form_valid(self, form):
        messages.success(self.request, 'Estado actualizado exitosamente')
        return super().form_valid(form)
