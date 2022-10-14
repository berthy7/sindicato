from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class Persona(models.Model):

    ci = models.CharField(max_length=25,null=True)
    ciFechaVencimiento = models.DateField(null=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(max_length=10,null=True)
    licenciaNro = models.CharField(max_length=25,null=True)
    licenciaCategoria = models.CharField(max_length=1,null=True)
    licenciaFechaVencimiento = models.DateField(null=True)

    lugarNacimiento = models.CharField(max_length=25, null=True)
    telefono = models.CharField(max_length=15, null=True)
    domicilio = models.CharField(max_length=50,null=True)
    latitud = models.CharField(max_length=50,null=True)
    longitud = models.CharField(max_length=50,null=True)
    tipo = models.CharField(max_length=50,null=True)
    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    fkrol = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)

    fklinea = models.IntegerField(null=True)
    fkinterno = models.IntegerField(null=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_persona"


class PersonaReferencia(models.Model):

    ci = models.CharField(max_length=25)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    categoria = models.CharField(max_length=20)
    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_personaReferencia"


