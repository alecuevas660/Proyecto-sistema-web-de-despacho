# Generated by Django 5.1.3 on 2024-11-24 16:02

import apps.users.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento_empleado',
            fields=[
                ('id_departamento', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre del Departamento')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'departamentos',
                'ordering': ['nombre'],
            },
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='departamento',
            field=models.ForeignKey(default=apps.users.models.Departamento_empleado.get_default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='users.departamento_empleado', verbose_name='Departamento'),
        ),
    ]
