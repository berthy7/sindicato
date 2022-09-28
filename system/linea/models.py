from django.db import models

# Create your models here.

class Linea(models.Model):
    codigo = models.CharField(max_length=25)
    razonSocial = models.CharField(max_length=25)
    denominacion = models.CharField(max_length=25)
    fechaFundacion = models.DateField()
    nroAutorizacion = models.CharField(max_length=25)
    descripcionRuta = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "linea"