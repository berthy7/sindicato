# Generated by Django 4.1.1 on 2022-10-19 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('incidente', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidente',
            name='fkpersona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.persona'),
        ),
        migrations.AddField(
            model_name='incidente',
            name='fktipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidente.incidentetipo'),
        ),
        migrations.AddField(
            model_name='incidente',
            name='fkusuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
