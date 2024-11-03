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
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar productos con stock bajo
        productos_stock_bajo = Product.objects.filter(
            stock_variables__cantidad_stock__lte=models.F('stock_minimo')
        ).distinct()
        context['productos_stock_bajo'] = productos_stock_bajo
        return context

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventario/product_list.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros
        filtro_stock = self.request.GET.get('stock')
        if filtro_stock == 'bajo':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__lte=models.F('stock_minimo')
            )
        elif filtro_stock == 'normal':
            queryset = queryset.filter(
                stock_variables__cantidad_stock__gt=models.F('stock_minimo')
            )
        
        # Búsqueda
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.distinct()

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
