from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from apps.ordenes.models import OrdenDespacho, DetalleOrden, EstadoOrden
from apps.ordenes.forms import OrdenDespachoForm, DetalleOrdenFormSet

class OrdenDespachoListView(LoginRequiredMixin, ListView):
    model = OrdenDespacho
    template_name = 'ordenes/orden_list.html'
    context_object_name = 'ordenes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'client':
            queryset = queryset.filter(cliente=self.request.user)
        
        # Búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(numero_orden__icontains=search)
        
        return queryset.select_related('cliente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = EstadoOrden.CHOICES
        return context

class OrdenDespachoCreateView(LoginRequiredMixin, CreateView):
    model = OrdenDespacho
    form_class = OrdenDespachoForm
    template_name = 'ordenes/orden_form.html'
    success_url = reverse_lazy('ordenes:orden_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalles'] = DetalleOrdenFormSet(self.request.POST)
        else:
            context['detalles'] = DetalleOrdenFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles']
        
        try:
            with transaction.atomic():
                # Guardar la orden
                self.object = form.save(commit=False)
                self.object.cliente = self.request.user
                self.object.save()

                # Validar y guardar los detalles
                if detalles_formset.is_valid():
                    detalles = detalles_formset.save(commit=False)
                    for detalle in detalles:
                        detalle.orden = self.object
                        detalle.precio_unitario = detalle.producto.price
                        detalle.save()
                    
                    # Actualizar el total de la orden
                    self.object.actualizar_total()
                else:
                    raise ValidationError('Error en los detalles de la orden')

                messages.success(self.request, 'Orden creada exitosamente')
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear la orden: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrija los errores en el formulario')
        return super().form_invalid(form)

class OrdenDespachoDetailView(LoginRequiredMixin, DetailView):
    model = OrdenDespacho
    template_name = 'ordenes/orden_detail.html'
    context_object_name = 'orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context 

class OrdenDespachoUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenDespacho
    form_class = OrdenDespachoForm
    template_name = 'ordenes/orden_form.html'
    success_url = reverse_lazy('ordenes:orden_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalles'] = DetalleOrdenFormSet(self.request.POST, instance=self.object)
        else:
            context['detalles'] = DetalleOrdenFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles']
        
        try:
            with transaction.atomic():
                self.object = form.save()
                if detalles_formset.is_valid():
                    detalles_formset.save()
                    self.object.actualizar_total()
                else:
                    raise ValidationError('Error en los detalles de la orden')

                messages.success(self.request, 'Orden actualizada exitosamente')
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar la orden: {str(e)}')
            return self.form_invalid(form)

class OrdenDespachoDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdenDespacho
    template_name = 'ordenes/orden_confirm_delete.html'
    success_url = reverse_lazy('ordenes:orden_list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Orden eliminada exitosamente')
            return response
        except Exception as e:
            messages.error(request, f'Error al eliminar la orden: {str(e)}')
            return redirect('ordenes:orden_list')

class EstadoUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenDespacho
    fields = ['estado']
    template_name = 'ordenes/estado_update.html'
    success_url = reverse_lazy('ordenes:orden_list')

    def form_valid(self, form):
        messages.success(self.request, 'Estado actualizado exitosamente')
        return super().form_valid(form)

@login_required
def exportar_despachos(request):
    # Implementar la lógica de exportación
    pass

@login_required
def configurar_reporte(request):
    # Implementar la lógica de configuración de reportes
    pass