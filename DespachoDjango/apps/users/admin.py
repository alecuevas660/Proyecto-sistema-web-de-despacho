# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClienteProfile, TransportistaProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nombre', 'apellido', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email',)

@admin.register(ClienteProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion_envio')

@admin.register(TransportistaProfile)
class TransportistaProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'licencia', 'disponibilidad')
