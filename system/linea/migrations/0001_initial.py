# Generated by Django 4.1.1 on 2022-10-19 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehiculo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('observacion', models.CharField(max_length=50, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'system_interno',
            },
        ),
        migrations.CreateModel(
            name='InternoPersona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaAsignacion', models.DateField(null=True)),
                ('fechaRetiro', models.DateField(null=True)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'system_internoPersona',
            },
        ),
        migrations.CreateModel(
            name='InternoVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaAsignacion', models.DateField(null=True)),
                ('fechaRetiro', models.DateField(null=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'system_internoVehiculo',
            },
        ),
        migrations.CreateModel(
            name='Linea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25)),
                ('razonSocial', models.CharField(max_length=25)),
                ('fechaFundacion', models.DateField()),
                ('ubicacion', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('apellidos', models.CharField(max_length=50, null=True)),
                ('celular', models.CharField(max_length=15, null=True)),
                ('internos', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'system_linea',
            },
        ),
        migrations.CreateModel(
            name='LineaVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaRetiro', models.DateField(null=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
                ('fklinea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='linea.linea')),
                ('fkvehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculo.vehiculo')),
            ],
            options={
                'db_table': 'system_lineaVehiculo',
            },
        ),
        migrations.CreateModel(
            name='LineaPersona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaRetiro', models.DateField(null=True)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fklinea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='linea.linea')),
            ],
            options={
                'db_table': 'system_lineaPersona',
            },
        ),
    ]
