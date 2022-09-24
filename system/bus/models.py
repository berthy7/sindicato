from django.db import models
from system.administracion.condominio.models import Condominio

# Create your models here.

class Bus(models.Model):

    placa = models.CharField(max_length=25)
    modelo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=25)
    año = models.IntegerField(null=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "bus"