from django.db import models
from system.vehiculoCategoria.models import VehiculoCategoria

# Create your models here.


class Vehiculo(models.Model):
    interno = models.IntegerField(null=True)
    placa = models.CharField(max_length=25)
    modelo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=25)
    pais = models.CharField(max_length=25, null=True)
    combustible = models.CharField(max_length=25, null=True)
    año = models.IntegerField(null=True)
    fkcategoria = models.ForeignKey(VehiculoCategoria, on_delete=models.CASCADE)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_vehiculo"