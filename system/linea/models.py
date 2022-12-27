from django.db import models
from system.vehiculo.models import Vehiculo
from system.persona.models import Persona
from django.contrib.auth.models import User

# Create your models here.

class Linea(models.Model):
    codigo = models.CharField(max_length=25)
    razonSocial = models.CharField(max_length=25)
    fechaFundacion = models.DateField()
    ubicacion = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50,null=True)
    apellidos = models.CharField(max_length=50,null=True)
    celular = models.CharField(max_length=15, null=True)
    mapa = models.CharField(max_length=255, null=True)
    fotoOficina = models.CharField(max_length=255, null=True)

    internos = models.IntegerField()
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_linea"


class Interno(models.Model):
    numero = models.IntegerField()
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fkpersona = models.ForeignKey(Persona,null=True, on_delete=models.CASCADE)
    fkvehiculo = models.ForeignKey(Vehiculo, null=True,on_delete=models.CASCADE)
    observacion = models.CharField(max_length=50, null= True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_interno"

class LineaVehiculo(models.Model):
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fkinterno = models.ForeignKey(Interno, on_delete=models.CASCADE,null=True)
    fkvehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fechaRetiro = models.DateField(null=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_lineaVehiculo"

class LineaPersona(models.Model):

    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fklinea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    fechaRetiro = models.DateField(null=True)
    tipoPersona = models.CharField(max_length=25, null=True)

    fechar = models.DateTimeField(auto_now_add=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_lineaPersona"

class InternoVehiculo(models.Model):
    fkinterno = models.ForeignKey(Interno, on_delete=models.CASCADE)
    fkvehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    fechaAsignacion = models.DateField(null=True)
    fechaRetiro = models.DateField(null=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fechar = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "system_internoVehiculo"

class InternoPersona(models.Model):
    fklinea = models.ForeignKey(Linea,null=True, on_delete=models.CASCADE)
    fkinterno = models.ForeignKey(Interno,null=True,  on_delete=models.CASCADE)
    fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipoPersona = models.CharField(max_length=25, null=True)

    fechaAsignacion = models.DateField(null=True)
    fechaRetiro = models.DateField(null=True)

    fechar = models.DateTimeField(auto_now_add=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_internoPersona"