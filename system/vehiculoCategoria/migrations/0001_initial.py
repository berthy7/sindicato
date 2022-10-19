# Generated by Django 4.1.1 on 2022-10-16 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VehiculoCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'system_vehiculoCategoria',
            },
        ),
    ]
