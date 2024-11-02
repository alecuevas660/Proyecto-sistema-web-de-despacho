"""
Este módulo define un sistema de gestión de usuarios, 
incluyendo un gestor de usuarios personalizado,
un modelo de usuario, y modelos para transportistas y clientes.
"""

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

# Administrador personalizado para el modelo User
class CustomUserManager(UserManager):
    """
    Gestor de usuarios personalizado para el modelo User.
    Proporciona métodos para crear usuarios y superusuarios.
    """
    def _create_user(self, username, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el email y la contraseña proporcionados.
        
        Args:
            username (str): El nombre de usuario.
            email (str): El email del usuario.
            password (str): La contraseña del usuario.
            **extra_fields: Otros campos adicionales para el usuario.
        
        Raises:
            ValueError: Si no se proporciona un email.
        
        Returns:
            User: El usuario creado.
        """
        if not email:
            raise ValueError('El email es necesario')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        """
        Crea un usuario normal.
        
        Args:
            username (str): El nombre de usuario.
            email (str): El email del usuario.
            password (str): La contraseña del usuario.
            **extra_fields: Otros campos adicionales para el usuario.
        
        Returns:
            User: El usuario creado.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        """
        Crea un superusuario.
        
        Args:
            username (str): El nombre de usuario.
            email (str): El email del superusuario.
            password (str): La contraseña del superusuario.
            **extra_fields: Otros campos adicionales para el superusuario.
        
        Returns:
            User: El superusuario creado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


# Modelo de usuario personalizado
class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que utiliza email como nombre de usuario.
    Extiende AbstractBaseUser y PermissionsMixin para manejar autenticación y permisos.
    
    Attributes:
        id (UUIDField): Identificador único del usuario.
        email (EmailField): Email único del usuario.
        username (CharField): Nombre de usuario.
        avatar (ImageField): Avatar del usuario.
        is_active (BooleanField): Indica si el usuario está activo.
        is_superuser (BooleanField): Indica si el usuario es un superusuario.
        is_staff (BooleanField): Indica si el usuario tiene acceso al admin.
        date_joined (DateTimeField): Fecha y hora de creación del usuario.
        last_login (DateTimeField): Fecha y hora del último inicio de sesión.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='uploads/avatars')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """
        Configuración de la tabla para el modelo User.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'user_account'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# Modelo de transportista
class Transportista(models.Model):
    """
    Modelo que representa a un transportista.
    
    Attributes:
        id (UUIDField): Identificador único del transportista.
        nombre (CharField): Nombre del transportista.
        contacto (CharField): Información de contacto del transportista.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)

    class Meta:
        """
        Configuración de la tabla para el modelo Transportista.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'transportistas'
        verbose_name = 'Transportista'
        verbose_name_plural = 'Transportistas'


# Modelo de cliente
class Cliente(models.Model):
    """
    Modelo que representa a un cliente.
    
    Attributes:
        id (UUIDField): Identificador único del cliente.
        nombre (CharField): Nombre del cliente.
        apellido (CharField): Apellido del cliente.
        direccion_envio (CharField): Dirección de envío del cliente.
        contacto (CharField): Información de contacto del cliente.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    direccion_envio = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)

    class Meta:
        """
        Configuración de la tabla para el modelo Cliente.
        
        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
            verbose_name (str): Nombre legible del modelo en singular.
            verbose_name_plural (str): Nombre legible del modelo en plural.
        """
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
