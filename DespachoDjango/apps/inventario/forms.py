from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Categoria, StockVariable

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'categoria', 'description', 'price', 'stock_minimo', 'activo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'data-live-search': 'true'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del producto'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(activo=True)
        
        # Agregar mensajes de ayuda
        self.fields['name'].help_text = 'El nombre debe ser único en la categoría seleccionada'
        self.fields['price'].help_text = 'Ingrese un precio mayor a 0'
        self.fields['stock_minimo'].help_text = 'Cantidad mínima antes de mostrar alertas'

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        
        # Validar caracteres especiales
        if not name.replace(' ', '').isalnum():
            raise ValidationError('El nombre solo puede contener letras, números y espacios.')
        
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError('El precio es obligatorio.')
        if price <= 0:
            raise ValidationError('El precio debe ser mayor que 0.')
        if price > 999999.99:
            raise ValidationError('El precio no puede ser mayor a 999,999.99.')
        return price

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is None:
            raise ValidationError('El stock mínimo es obligatorio.')
        if stock_minimo < 0:
            raise ValidationError('El stock mínimo no puede ser negativo.')
        if stock_minimo > 9999:
            raise ValidationError('El stock mínimo no puede ser mayor a 9,999.')
        return stock_minimo

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        categoria = cleaned_data.get('categoria')

        if name and categoria:
            # Verificar duplicados case-insensitive
            exists = Product.objects.filter(
                name__iexact=name,
                categoria=categoria
            )
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            
            if exists.exists():
                raise ValidationError({
                    'name': f'Ya existe un producto llamado "{name}" en la categoría {categoria.nombre}.'
                })

        return cleaned_data

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = StockVariable
        fields = ['cantidad_stock', 'motivo']
        widgets = {
            'cantidad_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motivo de la actualización'
            })
        }

class ReporteInventarioForm(forms.Form):
    ORDEN_CHOICES = [
        ('nombre', 'Nombre'),
        ('categoria', 'Categoría'),
        ('stock', 'Stock'),
        ('precio', 'Precio'),
    ]
    
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.filter(activo=True),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    umbral_stock_bajo = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ordenar_por = forms.ChoiceField(
        choices=ORDEN_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    incluir_inactivos = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )