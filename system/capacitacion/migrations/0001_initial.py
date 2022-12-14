# Generated by Django 4.1.1 on 2022-10-19 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CapacitacionCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fkusuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'system_capacitacionCurso',
            },
        ),
        migrations.CreateModel(
            name='Capacitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('descripcion', models.CharField(max_length=100)),
                ('dictado', models.CharField(max_length=100)),
                ('fechar', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('fkcurso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capacitacion.capacitacioncurso')),
            ],
            options={
                'db_table': 'system_capacitacion',
            },
        ),
    ]
