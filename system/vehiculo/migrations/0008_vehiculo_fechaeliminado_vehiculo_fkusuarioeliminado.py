# Generated by Django 4.1.1 on 2023-02-04 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0007_vehiculotransferencia_fechaeliminado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='fechaEliminado',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='fkusuarioEliminado',
            field=models.IntegerField(null=True),
        ),
    ]
