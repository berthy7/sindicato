from django.db import models

# Create your models here.


class VehiculoCategoria(models.Model):

    nombre = models.CharField(max_length=25)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_vehiculoCategoria"