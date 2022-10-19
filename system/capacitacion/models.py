from django.db import models
from django.contrib.auth.models import User
from system.persona.models import Persona
from system.linea.models import Linea
# Create your models here.

class CapacitacionCurso(models.Model):

    nombre = models.CharField(max_length=25)

    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fechar = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_capacitacionCurso"


class Capacitacion(models.Model):
    fkcurso = models.ForeignKey(CapacitacionCurso, on_delete=models.CASCADE)
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

    descripcion = models.CharField(max_length=100)
    dictado = models.CharField(max_length=100)

    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fechar = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_capacitacion"



