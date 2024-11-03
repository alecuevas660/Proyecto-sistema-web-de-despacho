from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Q, F
from .models import Product, StockVariable
from django.contrib import messages

# Create your views here.

class InventarioListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventario/inventario_list.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener productos con stock bajo
        context['productos_stock_bajo'] = Product.objects.filter(
            stock_variables__cantidad_stock__lte=F('stock_minimo')
        ).distinct()
        
        # Obtener estadísticas
        context['total_productos'] = Product.objects.count()
        context['total_stock_bajo'] = context['productos_stock_bajo'].count()
        
        return context

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventario/product_list.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filtro de stock
        stock_filter = self.request.GET.get('stock')
        if stock_filter == 'bajo':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__lte=F('stock_minimo')
            )
        elif stock_filter == 'normal':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__gt=F('stock_minimo')
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
        context['search'] = self.request.GET.get('search', '')
        context['stock_filter'] = self.request.GET.get('stock', '')
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventario/product_form.html'
    fields = ['name', 'description', 'price', 'stock_minimo', 'activo']
    success_url = reverse_lazy('inventario:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Crear registro inicial de stock
        StockVariable.objects.create(
            producto=self.object,
            cantidad_stock=0,
            motivo='Registro inicial'
        )
        messages.success(self.request, 'Producto creado exitosamente.')
        return response

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'inventario/product_form.html'
    fields = ['name', 'description', 'price', 'stock_minimo', 'activo']
    success_url = reverse_lazy('inventario:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return response

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventario/product_confirm_delete.html'
    success_url = reverse_lazy('inventario:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
