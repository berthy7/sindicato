# Generated by Django 4.1.1 on 2022-11-11 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('linea', '0004_internopersona_fklinea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internopersona',
            name='fkinterno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='linea.interno'),
        ),
    ]
