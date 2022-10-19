# Generated by Django 4.1.1 on 2022-10-16 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persona', '0001_initial'),
        ('capacitacion', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='capacitacion',
            name='fkpersona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.persona'),
        ),
        migrations.AddField(
            model_name='capacitacion',
            name='fkusuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
