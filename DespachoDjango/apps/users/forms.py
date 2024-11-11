from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClienteProfile, EmployeeProfile

class ClienteForm(UserCreationForm):
    nombre_supermercado = forms.CharField(max_length=255)
    rut_empresa = forms.CharField(max_length=20)
    direccion_facturacion = forms.CharField(max_length=255)
    direccion_envio = forms.CharField(max_length=255)
    preferencias_envio = forms.CharField(widget=forms.Textarea, required=False)

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
                preferencias_envio=self.cleaned_data['preferencias_envio']
            )
        return user

class EmployeeForm(UserCreationForm):
    departamento = forms.CharField(max_length=100)
    cargo = forms.CharField(max_length=100)
    fecha_contratacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employee'
        user.is_staff = True
        if commit:
            user.save()
            EmployeeProfile.objects.create(
                user=user,
                departamento=self.cleaned_data['departamento'],
                cargo=self.cleaned_data['cargo'],
                fecha_contratacion=self.cleaned_data['fecha_contratacion']
            )
        return user 