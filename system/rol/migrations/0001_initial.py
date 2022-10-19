# Generated by Django 4.1.1 on 2022-10-19 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50, null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('icono', models.CharField(max_length=50)),
                ('categoria', models.CharField(max_length=20)),
                ('orden', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
                ('fkmodulo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rol.modulo')),
            ],
            options={
                'db_table': 'auth_modules',
            },
        ),
        migrations.CreateModel(
            name='Permisos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fkmodulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rol.modulo')),
                ('fkrol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'db_table': 'auth_permisos',
            },
        ),
    ]
