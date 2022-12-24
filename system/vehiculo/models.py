from django.db import models
from system.vehiculoCategoria.models import VehiculoCategoria

# Create your models here.


class Vehiculo(models.Model):
    placa = models.CharField(max_length=25)
    modelo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=25)
    combustible = models.CharField(max_length=25, null=True)
    año = models.IntegerField(null=True)
    fkcategoria = models.ForeignKey(VehiculoCategoria, on_delete=models.CASCADE)
    fklinea = models.IntegerField(null=True)
    fkinterno = models.IntegerField(null=True)

    ruat = models.CharField(max_length=255, null=True)
    fotofrontal = models.CharField(max_length=255, null=True)
    fotolateral = models.CharField(max_length=255, null=True)

    soat = models.CharField(max_length=255, null=True)
    soatVencimiento = models.DateField(null=True)
    inspeccion = models.CharField(max_length=255, null=True)
    inspeccionVencimiento = models.DateField(null=True)
    seguro = models.CharField(max_length=255, null=True)
    seguroVencimiento = models.DateField(null=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_vehiculo"