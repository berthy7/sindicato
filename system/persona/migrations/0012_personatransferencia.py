# Generated by Django 4.1.1 on 2022-12-29 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0011_persona_antecedentes_persona_fechar_persona_fotoagua_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonaTransferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fklinea', models.IntegerField()),
                ('linea', models.CharField(max_length=50)),
                ('fkinterno', models.IntegerField()),
                ('interno', models.CharField(max_length=50)),
                ('fkpersona', models.IntegerField()),
                ('persona', models.CharField(max_length=100)),
                ('fkpersonaTrans', models.IntegerField()),
                ('personaTrans', models.CharField(max_length=50)),
                ('nota', models.CharField(max_length=250, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'system_personaTransferencia',
            },
        ),
    ]