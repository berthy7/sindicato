# Generated by Django 4.1.1 on 2022-10-10 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('incidente', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidente',
            name='fkpersona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.persona'),
        ),
        migrations.AddField(
            model_name='incidente',
            name='fkusuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
