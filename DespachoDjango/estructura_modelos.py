# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Categorias(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField()
    activo = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categorias'


class ClienteProfiles(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    nombre_supermercado = models.CharField(max_length=255)
    rut_empresa = models.CharField(unique=True, max_length=20)
    direccion_facturacion = models.CharField(max_length=255)
    direccion_envio = models.CharField(max_length=255)
    contacto_nombre = models.CharField(max_length=150)
    contacto_telefono = models.CharField(max_length=17)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    historial_compras = models.JSONField()
    fecha_ultima_compra = models.DateTimeField(blank=True, null=True)
    total_compras = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'cliente_profiles'


class DetalleCompra(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    cantidad_productos = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    fecha_compra = models.DateTimeField()
    producto = models.ForeignKey('Products', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'detalle_compra'


class DetallesVenta(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    descuento = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    subtotal = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    producto = models.ForeignKey('Products', models.DO_NOTHING)
    venta = models.ForeignKey('Ventas', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'detalles_venta'
        unique_together = (('venta', 'producto'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EmployeeProfiles(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    supervisor = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_profiles'


class OrdenDespacho(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    direccion_entrega = models.TextField()
    fecha_creacion = models.DateTimeField()
    observaciones = models.TextField()
    cliente = models.ForeignKey('Users', models.DO_NOTHING)
    compra = models.ForeignKey(DetalleCompra, models.DO_NOTHING)
    transportista = models.ForeignKey('Users', models.DO_NOTHING, related_name='ordendespacho_transportista_set')

    class Meta:
        managed = False
        db_table = 'orden_despacho'


class Products(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    stock_minimo = models.PositiveIntegerField()
    activo = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products'
        unique_together = (('name', 'categoria'),)


class ReporteEnvios(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_envios = models.PositiveIntegerField()
    envios_completados = models.PositiveIntegerField()
    envios_pendientes = models.PositiveIntegerField()
    fecha_generacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reporte_envios'


class ReporteFinanciero(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_ventas = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_envios = models.PositiveIntegerField()
    fecha_generacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reporte_financiero'


class SeguimientoEnvio(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    estado_envio = models.CharField(max_length=20)
    ubicacion_actual = models.CharField(max_length=255)
    comentarios = models.TextField()
    fecha_actualizacion = models.DateTimeField()
    orden = models.ForeignKey(OrdenDespacho, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'seguimiento_envio'


class StockVariable(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    cantidad_stock = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    producto = models.ForeignKey(Products, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stock_variable'


class TransportistaProfiles(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    licencia = models.CharField(max_length=50)
    numero_licencia = models.CharField(unique=True, max_length=20)
    vehiculo = models.CharField(max_length=100)
    zona_cobertura = models.TextField()
    disponibilidad = models.BooleanField()
    entregas_completadas = models.PositiveIntegerField()
    calificacion_promedio = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'transportista_profiles'


class Users(models.Model):
    password = models.CharField(max_length=128)
    id = models.CharField(primary_key=True, max_length=32)
    email = models.CharField(unique=True, max_length=254)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    telefono = models.CharField(max_length=17)
    direccion = models.TextField()
    role = models.CharField(max_length=20)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersGroups(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_groups'
        unique_together = (('user', 'group'),)


class UsersUserPermissions(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_permissions'
        unique_together = (('user', 'permission'),)


class Ventas(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    numero_venta = models.CharField(unique=True, max_length=10)
    rut_cliente = models.CharField(max_length=12)
    metodo_pago = models.CharField(max_length=20)
    subtotal = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    impuestos = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    estado = models.CharField(max_length=20)
    notas = models.TextField()
    fecha_venta = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField()
    cliente = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    vendedor = models.ForeignKey(Users, models.DO_NOTHING, related_name='ventas_vendedor_set')

    class Meta:
        managed = False
        db_table = 'ventas'
