# Generated by Django 4.1.1 on 2022-12-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0008_persona_fechainscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='certificadoInscripcion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='memorandum',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
