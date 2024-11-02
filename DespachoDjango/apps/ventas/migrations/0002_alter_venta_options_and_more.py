# Generated by Django 5.1.2 on 2024-11-02 23:01

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_detallecompra_product_reporteenvios_and_more'),
        ('ventas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venta',
            options={'ordering': ['-fecha_venta'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
        migrations.AlterUniqueTogether(
            name='detalleventa',
            unique_together={('venta', 'producto')},
        ),
        migrations.RemoveField(
            model_name='venta',
            name='creado',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='nombre_cliente',
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='descuento',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Descuento'),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Precio Unitario'),
        ),
        migrations.AddField(
            model_name='venta',
            name='cliente',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'client'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='compras', to=settings.AUTH_USER_MODEL, verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='venta',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='venta',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True, verbose_name='Última Actualización'),
        ),
        migrations.AddField(
            model_name='venta',
            name='fecha_venta',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha de Venta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='impuestos',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Impuestos'),
        ),
        migrations.AddField(
            model_name='venta',
            name='notas',
            field=models.TextField(blank=True, verbose_name='Notas'),
        ),
        migrations.AddField(
            model_name='venta',
            name='numero_venta',
            field=models.CharField(default=1, editable=False, max_length=10, unique=True, verbose_name='Número de Venta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Subtotal'),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='cantidad',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ventas', to='inventario.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10, verbose_name='Subtotal'),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.venta', verbose_name='Venta'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='venta',
            name='metodo_pago',
            field=models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), ('otro', 'Otro')], default='efectivo', max_length=20, verbose_name='Método de Pago'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='rut_cliente',
            field=models.CharField(blank=True, max_length=12, verbose_name='RUT Cliente'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='vendedor',
            field=models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.PROTECT, related_name='ventas_realizadas', to=settings.AUTH_USER_MODEL, verbose_name='Vendedor'),
        ),
        migrations.AlterModelTable(
            name='detalleventa',
            table='detalles_venta',
        ),
        migrations.AlterModelTable(
            name='venta',
            table='ventas',
        ),
        migrations.RemoveField(
            model_name='detalleventa',
            name='precio',
        ),
    ]
