# Generated by Django 5.0.1 on 2024-12-21 03:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('correo_cliente', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(max_length=50)),
                ('telefono_cliente', models.CharField(max_length=15)),
                ('password_cliente', models.CharField(max_length=128)),
                ('puntos', models.IntegerField()),
                ('imagen_cliente', models.ImageField(null=True, upload_to='imagen_cliente')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'Cliente',
                'ordering': ['correo_cliente'],
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id_direccion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_direccion', models.CharField(max_length=50, null=True)),
                ('departamento', models.CharField(max_length=50)),
                ('numero_casa', models.IntegerField()),
                ('municipio', models.CharField(max_length=50, null=True)),
                ('calle', models.CharField(max_length=50)),
                ('punto_referencia', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direcciones', to='Cliente.cliente')),
            ],
            options={
                'verbose_name': 'Direccion',
                'verbose_name_plural': 'Direcciones',
                'db_table': 'Direccion',
                'ordering': ['id_direccion'],
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('total_pago', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tipo_pago', models.CharField(max_length=15)),
                ('correo_cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Cliente.cliente')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
                'db_table': 'Pago',
                'ordering': ['id_pago'],
            },
        ),
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id_reclamo', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion_reclamo', models.CharField(max_length=100)),
                ('fecha_reclamo', models.DateField()),
                ('correo_cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Cliente.cliente')),
            ],
            options={
                'verbose_name': 'Reclamo',
                'verbose_name_plural': 'Reclamos',
                'db_table': 'Reclamo',
                'ordering': ['id_reclamo'],
            },
        ),
    ]
