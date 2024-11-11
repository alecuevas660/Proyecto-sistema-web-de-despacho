# Generated by Django 5.1.2 on 2024-11-04 12:30

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('nombre', models.CharField(default='Usuario', max_length=150, verbose_name='Nombre')),
                ('apellido', models.CharField(default='Sin Apellido', max_length=150, verbose_name='Apellido')),
                ('telefono', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="El número debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Teléfono')),
                ('direccion', models.TextField(blank=True, verbose_name='Dirección')),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('client', 'Cliente'), ('transport', 'Transportista'), ('employee', 'Empleado')], default='client', max_length=20, verbose_name='Rol')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m/', verbose_name='Foto de Perfil')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superusuario')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Registro')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Último Acceso')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'users',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='ClienteProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='cliente_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre_supermercado', models.CharField(max_length=255, verbose_name='Nombre del Supermercado')),
                ('rut_empresa', models.CharField(max_length=20, unique=True, verbose_name='RUT Empresa')),
                ('direccion_facturacion', models.CharField(max_length=255, verbose_name='Dirección de Facturación')),
                ('direccion_envio', models.CharField(max_length=255, verbose_name='Dirección de Envío')),
                ('contacto_nombre', models.CharField(max_length=150, verbose_name='Nombre de Contacto')),
                ('contacto_telefono', models.CharField(max_length=17, verbose_name='Teléfono de Contacto')),
                ('limite_credito', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Límite de Crédito')),
                ('historial_compras', models.JSONField(blank=True, default=dict, verbose_name='Historial de Compras')),
                ('fecha_ultima_compra', models.DateTimeField(blank=True, null=True, verbose_name='Última Compra')),
                ('total_compras', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total en Compras')),
            ],
            options={
                'verbose_name': 'Perfil de Cliente',
                'verbose_name_plural': 'Perfiles de Clientes',
                'db_table': 'cliente_profiles',
            },
        ),
        migrations.CreateModel(
            name='TransportistaProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='transportista_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('licencia', models.CharField(choices=[('A', 'Clase A'), ('B', 'Clase B'), ('C', 'Clase C'), ('D', 'Clase D')], max_length=50, verbose_name='Licencia')),
                ('numero_licencia', models.CharField(max_length=20, unique=True, verbose_name='Número de Licencia')),
                ('vehiculo', models.CharField(max_length=100, verbose_name='Vehículo')),
                ('zona_cobertura', models.TextField(verbose_name='Zona de Cobertura')),
                ('disponibilidad', models.BooleanField(default=True, verbose_name='Disponible')),
                ('entregas_completadas', models.PositiveIntegerField(default=0, verbose_name='Entregas Completadas')),
                ('calificacion_promedio', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Calificación Promedio')),
            ],
            options={
                'verbose_name': 'Perfil de Transportista',
                'verbose_name_plural': 'Perfiles de Transportistas',
                'db_table': 'transportista_profiles',
            },
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employee_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('departamento', models.CharField(max_length=100, verbose_name='Departamento')),
                ('cargo', models.CharField(choices=[('gerente_logistica', 'Gerente de Logística'), ('gerente_financiero', 'Gerente Financiero'), ('encargado_inventario', 'Encargado de Inventario'), ('asistente_logistica', 'Asistente de Logística'), ('analista_datos', 'Analista de Datos')], max_length=100, verbose_name='Cargo')),
                ('fecha_contratacion', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de Contratación')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisados', to='users.employeeprofile')),
            ],
            options={
                'verbose_name': 'Perfil de Empleado',
                'verbose_name_plural': 'Perfiles de Empleados',
                'db_table': 'employee_profiles',
            },
        ),
    ]
