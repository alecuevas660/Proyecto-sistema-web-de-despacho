from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, ClienteProfile, EmployeeProfile, Departamento_empleado

class ClienteForm(UserCreationForm):
    nombre_supermercado = forms.CharField(max_length=255)
    rut_empresa = forms.CharField(max_length=20)
    direccion_facturacion = forms.CharField(max_length=255)
    direccion_envio = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'
        if commit:
            user.save()
            ClienteProfile.objects.create(
                user=user,
                nombre_supermercado=self.cleaned_data['nombre_supermercado'],
                rut_empresa=self.cleaned_data['rut_empresa'],
                direccion_facturacion=self.cleaned_data['direccion_facturacion'],
                direccion_envio=self.cleaned_data['direccion_envio'],
            )
        return user

class EmployeeForm(UserCreationForm):
    # Campos del usuario
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    nombre = forms.CharField(
        label='Nombre',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellido = forms.CharField(
        label='Apellido',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Campos del perfil de empleado
    departamento = forms.ModelChoiceField(
        queryset=Departamento_empleado.objects.all(),
        empty_label="Seleccione un departamento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cargo = forms.ChoiceField(
        choices=EmployeeProfile.ROLES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_contratacion = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employee'
        user.is_staff = True
        # Establecer el flag para evitar la creación automática del perfil
        setattr(user, '_dont_setup_profile', True)
        
        if commit:
            user.save()
            # Crear el perfil manualmente
            try:
                EmployeeProfile.objects.get(user=user)
            except EmployeeProfile.DoesNotExist:
                EmployeeProfile.objects.create(
                    user=user,
                    departamento=self.cleaned_data['departamento'],
                    cargo=self.cleaned_data['cargo'],
                    fecha_contratacion=self.cleaned_data['fecha_contratacion']
                )
        return user

class ClienteUpdateForm(ModelForm):
    nombre_supermercado = forms.CharField(max_length=255)
    rut_empresa = forms.CharField(max_length=20)
    direccion_facturacion = forms.CharField(max_length=255)
    direccion_envio = forms.CharField(max_length=255)
    contacto_nombre = forms.CharField(max_length=150)
    contacto_telefono = forms.CharField(max_length=17)
    email = forms.EmailField()
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'cliente_profile'):
            profile = self.instance.cliente_profile
            self.fields['nombre_supermercado'].initial = profile.nombre_supermercado
            self.fields['rut_empresa'].initial = profile.rut_empresa
            self.fields['direccion_facturacion'].initial = profile.direccion_facturacion
            self.fields['direccion_envio'].initial = profile.direccion_envio
            self.fields['contacto_nombre'].initial = profile.contacto_nombre
            self.fields['contacto_telefono'].initial = profile.contacto_telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = self.instance.cliente_profile
            profile.nombre_supermercado = self.cleaned_data['nombre_supermercado']
            profile.rut_empresa = self.cleaned_data['rut_empresa']
            profile.direccion_facturacion = self.cleaned_data['direccion_facturacion']
            profile.direccion_envio = self.cleaned_data['direccion_envio']
            profile.contacto_nombre = self.cleaned_data['contacto_nombre']
            profile.contacto_telefono = self.cleaned_data['contacto_telefono']
            profile.save()
        return user

class EmployeeUpdateForm(ModelForm):
    departamento = forms.CharField(max_length=100)
    cargo = forms.CharField(max_length=100)
    fecha_contratacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    nombre_contacto = forms.CharField(max_length=255)
    telefono_contacto = forms.CharField(max_length=20)
    email = forms.EmailField()
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'employee_profile'):
            profile = self.instance.employee_profile
            self.fields['departamento'].initial = profile.departamento
            self.fields['cargo'].initial = profile.cargo
            self.fields['fecha_contratacion'].initial = profile.fecha_contratacion
            self.fields['nombre_contacto'].initial = profile.nombre_contacto
            self.fields['telefono_contacto'].initial = profile.telefono_contacto

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = self.instance.employee_profile
            profile.departamento = self.cleaned_data['departamento']
            profile.cargo = self.cleaned_data['cargo']
            profile.fecha_contratacion = self.cleaned_data['fecha_contratacion']
            profile.nombre_contacto = self.cleaned_data['nombre_contacto']
            profile.telefono_contacto = self.cleaned_data['telefono_contacto']
            profile.save()
        return user