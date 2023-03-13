# Generated by Django 4.1.1 on 2023-02-21 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0019_personatransferencia_fkpersonatranssalida_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personatransferencia',
            name='fkusuarioSalida',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='personatransferencia',
            name='usuarioSalida',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='personatransferencia',
            name='personaTrans',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='personatransferencia',
            name='personaTransSalida',
            field=models.CharField(max_length=100, null=True),
        ),
    ]