# Generated by Django 4.1.1 on 2022-12-03 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='ruat',
            field=models.CharField(max_length=255, null=True),
        ),
    ]