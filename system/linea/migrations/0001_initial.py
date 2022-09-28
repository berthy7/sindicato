# Generated by Django 4.1.1 on 2022-09-27 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Linea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25)),
                ('razonSocial', models.CharField(max_length=25)),
                ('denominacion', models.CharField(max_length=25)),
                ('fechaFundacion', models.DateField()),
                ('nroAutorizacion', models.CharField(max_length=25)),
                ('descripcionRuta', models.CharField(max_length=50)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'linea',
            },
        ),
    ]
