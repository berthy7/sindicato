# Generated by Django 4.1.1 on 2022-12-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0010_persona_fechaeliminado_persona_fkusuarioeliminado'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='antecedentes',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='fechar',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='fotoAgua',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='fotoLuz',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
