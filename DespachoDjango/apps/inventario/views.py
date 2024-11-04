from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Q, F
from .models import Product, StockVariable, Categoria
from django.contrib import messages
from .forms import ProductForm, StockUpdateForm
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError

# Create your views here.

class InventarioListView(ListView):
    model = Product
    template_name = 'inventario/inventario_list.html'
    context_object_name = 'productos'
    paginate_by = 10  # Mostrar 10 productos por página

    def get_queryset(self):
        queryset = Product.objects.select_related('categoria').all()

        # Filtro de categoría
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)

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
        
        # Obtener todos los productos con su último stock
        productos = self.get_queryset()  # Obtener los productos filtrados
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
        context['categorias'] = Categoria.objects.filter(activo=True)  # Obtener categorías activas para el filtro
        
        return context

class ProductListView(ListView):
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
