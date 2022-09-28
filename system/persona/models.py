from django.db import models
from system.linea.models import Linea

# Create your models here.


class Persona(models.Model):

    ci = models.CharField(max_length=25)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(max_length=10)
    licenciaNro = models.CharField(max_length=25)
    licenciaCategoria = models.CharField(max_length=1)
    licenciaFechaVencimiento = models.DateField()
    lugarNacimiento = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    latitud = models.CharField(max_length=50)
    longitud = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_persona"


class PersonaFamiliar(models.Model):

    ci = models.CharField(max_length=25)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    FechaNacimiento  = models.DateField()
    lugarNacimiento = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10)
    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_personaFamiliar"


class PersonaLinea(models.Model):

    Fecha  = models.DateField()
    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_personaLinea"