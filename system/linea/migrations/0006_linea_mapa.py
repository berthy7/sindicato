# Generated by Django 4.1.1 on 2022-12-05 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linea', '0005_alter_internopersona_fkinterno'),
    ]

    operations = [
        migrations.AddField(
            model_name='linea',
            name='mapa',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
