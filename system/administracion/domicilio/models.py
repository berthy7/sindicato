from django.db import models
from system.administracion.condominio.models import Condominio

# Create your models here.


class Domicilio(models.Model):

    codigo = models.CharField(max_length=100)
    numero = models.IntegerField(null=True)
    ubicacion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100,null=True)
    fkcondominio = models.ForeignKey(Condominio,on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "administracion_domilicio"