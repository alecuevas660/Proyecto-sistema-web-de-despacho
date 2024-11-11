# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, ClienteProfile, TransportistaProfile, EmployeeProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nombre', 'apellido', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email',)
    
    # Definimos los fieldsets personalizados
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información Personal'), {'fields': ('nombre', 'apellido', 'telefono', 'direccion', 'avatar')}),
        (_('Permisos'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos para cuando se crea un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombre', 'apellido', 'role'),
        }),
    )

@admin.register(ClienteProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_supermercado', 'rut_empresa', 'direccion_envio')
    search_fields = ('nombre_supermercado', 'rut_empresa', 'user__email')

@admin.register(TransportistaProfile)
class TransportistaProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'licencia', 'disponibilidad')
    list_filter = ('disponibilidad', 'licencia')

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'departamento', 'cargo', 'fecha_contratacion')
    search_fields = ('user__email', 'user__nombre', 'departamento', 'cargo')
    list_filter = ('departamento', 'cargo', 'fecha_contratacion')
