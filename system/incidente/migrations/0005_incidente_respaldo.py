# Generated by Django 4.1.1 on 2022-12-04 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidente', '0004_remove_incidente_otro'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidente',
            name='respaldo',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
