from django.db import models
from django.contrib.auth.models import User, Group
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Persona(models.Model):

    fechaInscripcion = models.DateField(null=True)
    ci = models.CharField(max_length=25,null=True)
    fechaNacimiento = models.DateField(null=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(max_length=10,null=True)
    licenciaNro = models.CharField(max_length=25,null=True)
    licenciaCategoria = models.CharField(max_length=1,null=True)
    licenciaFechaVencimiento = models.DateField(null=True)
    socioConductor = models.CharField(max_length=5, null=True)

    foto = models.CharField(max_length=255, null=True)
    fotoCi = models.CharField(max_length=255, null=True)
    fotoLicencia = models.CharField(max_length=255, null=True)

    certificadoInscripcion = models.CharField(max_length=255, null=True)
    memorandum = models.CharField(max_length=255, null=True)

    antecedentes = models.CharField(max_length=255, null=True)
    fotoLuz = models.CharField(max_length=255, null=True)
    fotoAgua = models.CharField(max_length=255, null=True)


    lugarNacimiento = models.CharField(max_length=25, null=True)
    telefono = models.CharField(max_length=15, null=True)
    domicilio = models.CharField(max_length=50,null=True)
    latitud = models.CharField(max_length=50,null=True)
    longitud = models.CharField(max_length=50,null=True)
    tipo = models.CharField(max_length=50,null=True)
    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='fkusuario')
    fkrol = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    fechar = models.DateTimeField(auto_now_add=True,null=True)

    fkusuarioCreacion = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='fkusuarioCreacion')

    fklinea = models.IntegerField(null=True)
    fkinterno = models.IntegerField(null=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fkusuarioEliminado = models.IntegerField(null=True)
    fechaEliminado = models.DateTimeField(null=True)

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


class PersonaTransferencia(models.Model):
    fklinea = models.IntegerField()
    linea = models.CharField(max_length=50)
    fkinterno = models.IntegerField()
    interno = models.CharField(max_length=50)

    fkpersona = models.IntegerField()
    persona = models.CharField(max_length=100)

    fkpersonaTrans = models.IntegerField(null=True)
    personaTrans = models.CharField(max_length=50)

    nota = models.CharField(max_length=250,null=True)

    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    fechar = models.DateTimeField(auto_now_add=True,null=True)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "system_personaTransferencia"