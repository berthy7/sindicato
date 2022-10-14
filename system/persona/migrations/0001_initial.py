# Generated by Django 4.1.1 on 2022-10-14 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.CharField(max_length=25, null=True)),
                ('ciFechaVencimiento', models.DateField(null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('genero', models.CharField(max_length=10, null=True)),
                ('licenciaNro', models.CharField(max_length=25, null=True)),
                ('licenciaCategoria', models.CharField(max_length=1, null=True)),
                ('licenciaFechaVencimiento', models.DateField(null=True)),
                ('lugarNacimiento', models.CharField(max_length=25, null=True)),
                ('telefono', models.CharField(max_length=15, null=True)),
                ('domicilio', models.CharField(max_length=50, null=True)),
                ('latitud', models.CharField(max_length=50, null=True)),
                ('longitud', models.CharField(max_length=50, null=True)),
                ('tipo', models.CharField(max_length=50, null=True)),
                ('fklinea', models.IntegerField(null=True)),
                ('fkinterno', models.IntegerField(null=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fkrol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('fkusuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'system_persona',
            },
        ),
        migrations.CreateModel(
            name='PersonaReferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.CharField(max_length=25)),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('genero', models.CharField(max_length=10)),
                ('telefono', models.CharField(max_length=15)),
                ('categoria', models.CharField(max_length=20)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fkpersona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.persona')),
            ],
            options={
                'db_table': 'system_personaReferencia',
            },
        ),
    ]
