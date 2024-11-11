from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User, ClienteProfile, EmployeeProfile

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para el sistema'

    def handle(self, *args, **kwargs):
        # Crear clientes (supermercados)
        clientes = [
            {
                'email': 'super1@example.com',
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'password': 'clave123',
                'role': 'client',
                'profile': {
                    'nombre_supermercado': 'Supermercado El Sol',
                    'rut_empresa': '12345678-9',
                    'direccion_facturacion': 'Av. Principal 123',
                    'direccion_envio': 'Av. Principal 123',
                    'contacto_nombre': 'Juan Pérez',
                    'contacto_telefono': '+56912345678'
                }
            },
            # Agregar más clientes aquí
        ]

        # Crear empleados
        empleados = [
            {
                'email': 'empleado1@caiman.com',
                'nombre': 'María',
                'apellido': 'López',
                'password': 'clave123',
                'role': 'employee',
                'profile': {
                    'departamento': 'Logística',
                    'cargo': 'gerente_logistica',
                    'fecha_contratacion': timezone.now().date()
                }
            },
            # Agregar más empleados aquí
        ]

        for cliente in clientes:
            profile_data = cliente.pop('profile')
            user = User.objects.create_user(**cliente)
            profile = user.cliente_profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
            self.stdout.write(f'Cliente creado: {user.email}')

        for empleado in empleados:
            profile_data = empleado.pop('profile')
            user = User.objects.create_user(**empleado)
            profile = user.employee_profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
            self.stdout.write(f'Empleado creado: {user.email}') 