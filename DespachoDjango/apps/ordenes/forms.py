from django import forms
from django.forms import inlineformset_factory
from apps.ordenes.models import OrdenDespacho, DetalleOrden
from apps.inventario.models import Product

class OrdenDespachoForm(forms.ModelForm):
    class Meta:
        model = OrdenDespacho
        fields = ['direccion_entrega', 'observaciones']
        widgets = {
            'direccion_entrega': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la dirección de entrega'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }

class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control select2',
                'required': 'required'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo productos activos
        self.fields['producto'].queryset = Product.objects.filter(activo=True)

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if producto and cantidad:
            stock_actual = producto.get_stock_actual()
            if cantidad > stock_actual:
                raise forms.ValidationError(f'Stock insuficiente. Disponible: {stock_actual}')
            
            # Establecer el precio unitario automáticamente
            cleaned_data['precio_unitario'] = producto.price

        return cleaned_data

DetalleOrdenFormSet = inlineformset_factory(
    OrdenDespacho,
    DetalleOrden,
    form=DetalleOrdenForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
) 