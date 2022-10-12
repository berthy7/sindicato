from django.db import models
from django.contrib.auth.models import User
from system.persona.models import Persona
# Create your models here.



class Incidente(models.Model):

    nroIncidente = models.IntegerField(null=True)
    fechaIncidente = models.DateTimeField(null=True)
    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    codigoUnidad = models.CharField(max_length=25)
    clasificacion = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=25)
    acciones = models.CharField(max_length=25)
    costo = models.IntegerField(null=True)
    estados = models.CharField(max_length=25)

    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fechar = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_incidente"
