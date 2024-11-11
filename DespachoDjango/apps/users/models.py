import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    """Gestor personalizado para el modelo de usuario."""

    def _create_user(self, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el email y contraseña dados.
        """
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Crear perfil automáticamente según el rol
        if user.role == 'client':
            ClienteProfile.objects.create(user=user)
        elif user.role == 'transport':
            TransportistaProfile.objects.create(user=user)
        elif user.role == 'employee':
            EmployeeProfile.objects.create(user=user)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Crea un usuario normal."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """Crea un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado que usa email como identificador principal."""

    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        CLIENT = 'client', 'Cliente'
        TRANSPORT = 'transport', 'Transportista'
        EMPLOYEE = 'employee', 'Empleado'

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )

    # Campos básicos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Correo Electrónico', unique=True)
    nombre = models.CharField('Nombre', max_length=150, default="Usuario")
    apellido = models.CharField('Apellido', max_length=150, default="Sin Apellido")
    telefono = models.CharField(
        'Teléfono',
        validators=[phone_regex],
        max_length=17,
        blank=True
    )
    direccion = models.TextField('Dirección', blank=True)
    role = models.CharField(
        'Rol',
        max_length=20,
        choices=Roles.choices,
        default=Roles.CLIENT
    )
    avatar = models.ImageField(
        'Foto de Perfil',
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True
    )

    # Campos de estado
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Superusuario', default=False)
    date_joined = models.DateTimeField('Fecha de Registro', default=timezone.now)
    last_login = models.DateTimeField('Último Acceso', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.nombre} {self.apellido}".strip()

    def get_short_name(self):
        """Retorna el nombre corto del usuario."""
        return self.nombre

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envía un email al usuario."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_client(self):
        return self.role == self.Roles.CLIENT

    @property
    def is_transport(self):
        return self.role == self.Roles.TRANSPORT

    @property
    def is_employee(self):
        return self.role == self.Roles.EMPLOYEE

class ClienteProfile(models.Model):
    """Perfil extendido para usuarios con rol de cliente (supermercados)."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='cliente_profile'
    )
    nombre_supermercado = models.CharField('Nombre del Supermercado', max_length=255)
    rut_empresa = models.CharField('RUT Empresa', max_length=20, unique=True)
    direccion_facturacion = models.CharField('Dirección de Facturación', max_length=255)
    direccion_envio = models.CharField('Dirección de Envío', max_length=255)
    contacto_nombre = models.CharField('Nombre de Contacto', max_length=150)
    contacto_telefono = models.CharField('Teléfono de Contacto', max_length=17)
    limite_credito = models.DecimalField(
        'Límite de Crédito',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    historial_compras = models.JSONField(
        'Historial de Compras',
        default=dict,
        blank=True
    )
    fecha_ultima_compra = models.DateTimeField(
        'Última Compra',
        null=True,
        blank=True
    )
    total_compras = models.DecimalField(
        'Total en Compras',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'cliente_profiles'
        verbose_name = 'Perfil de Cliente'
        verbose_name_plural = 'Perfiles de Clientes'

    def __str__(self):
        return f"{self.nombre_supermercado} ({self.user.email})"

class TransportistaProfile(models.Model):
    """Perfil extendido para usuarios con rol de transportista."""

    TIPO_LICENCIA_CHOICES = [
        ('A', 'Clase A'),
        ('B', 'Clase B'),
        ('C', 'Clase C'),
        ('D', 'Clase D'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='transportista_profile'
    )
    licencia = models.CharField(
        'Licencia',
        max_length=50,
        choices=TIPO_LICENCIA_CHOICES
    )
    numero_licencia = models.CharField(
        'Número de Licencia',
        max_length=20,
        unique=True
    )
    vehiculo = models.CharField('Vehículo', max_length=100)
    zona_cobertura = models.TextField('Zona de Cobertura')
    disponibilidad = models.BooleanField('Disponible', default=True)
    entregas_completadas = models.PositiveIntegerField(
        'Entregas Completadas',
        default=0
    )
    calificacion_promedio = models.DecimalField(
        'Calificación Promedio',
        max_digits=3,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'transportista_profiles'
        verbose_name = 'Perfil de Transportista'
        verbose_name_plural = 'Perfiles de Transportistas'

    def __str__(self):
        return f"Perfil de Transportista: {self.user.get_full_name()}"

    def actualizar_calificacion(self, nueva_calificacion):
        """Actualiza la calificación promedio del transportista."""
        self.calificacion_promedio = (
            (self.calificacion_promedio * self.entregas_completadas + nueva_calificacion) /
            (self.entregas_completadas + 1)
        )
        self.entregas_completadas += 1
        self.save()

class EmployeeProfile(models.Model):
    """Perfil extendido para usuarios con rol de empleado."""
    
    ROLES_CHOICES = [
        ('gerente_logistica', 'Gerente de Logística'),
        ('gerente_financiero', 'Gerente Financiero'),
        ('encargado_inventario', 'Encargado de Inventario'),
        ('asistente_logistica', 'Asistente de Logística'),
        ('analista_datos', 'Analista de Datos'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employee_profile'
    )
    departamento = models.CharField('Departamento', max_length=100)
    cargo = models.CharField('Cargo', max_length=100, choices=ROLES_CHOICES)
    fecha_contratacion = models.DateField('Fecha de Contratación', default=timezone.now)
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervisados'
    )

    class Meta:
        db_table = 'employee_profiles'
        verbose_name = 'Perfil de Empleado'
        verbose_name_plural = 'Perfiles de Empleados'

    def __str__(self):
        return f"Perfil de Empleado: {self.user.get_full_name()}"

    def get_cargo_display(self):
        """Retorna el nombre legible del cargo"""
        return dict(self.ROLES_CHOICES).get(self.cargo, self.cargo)
