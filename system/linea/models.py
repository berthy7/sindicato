from django.db import models
from system.vehiculo.models import Vehiculo
from system.persona.models import Persona
from django.contrib.auth.models import User

# Create your models here.

class Linea(models.Model):
    codigo = models.CharField(max_length=25)
    razonSocial = models.CharField(max_length=25)
    denominacion = models.CharField(max_length=25)
    fechaFundacion = models.DateField()
    nroAutorizacion = models.CharField(max_length=25)
    descripcionRuta = models.CharField(max_length=50)
    internos = models.IntegerField()
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_linea"

class LineaInterno(models.Model):
    numero = models.IntegerField()
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fkpersona = models.ForeignKey(Persona,null=True, on_delete=models.CASCADE)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_lineaIterno"


class LineaVehiculo(models.Model):
    fkinterno = models.ForeignKey(LineaInterno, on_delete=models.CASCADE)
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fkvehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fechaAsignacion = models.DateField(null=True)
    fechaRetiro = models.DateField(null=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_lineaVehiculo"

class LineaPersona(models.Model):

    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fechaAsignacion = models.DateField(null=True)
    fechaRetiro = models.DateField(null=True)

    fechar = models.DateTimeField(auto_now_add=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_lineaPersona"
