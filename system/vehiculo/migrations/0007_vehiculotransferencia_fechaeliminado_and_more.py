# Generated by Django 4.1.1 on 2023-01-14 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0006_vehiculotransferencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculotransferencia',
            name='fechaEliminado',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculotransferencia',
            name='fkusuarioEliminado',
            field=models.IntegerField(null=True),
        ),
    ]
