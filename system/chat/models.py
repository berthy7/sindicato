from django.db import models
from django.contrib.auth.models import User
from system.persona.models import Persona
from system.linea.models import Linea

# Create your models here.

class Chat(models.Model):
    fklinea = models.ForeignKey(Linea, null=True, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    emisorId = models.IntegerField()
    emisor = models.CharField(max_length=200)
    mensaje = models.CharField(max_length=200)
    mensajeAdjunto = models.CharField(max_length=255, null=True)

    fechar = models.DateTimeField(null=True)
    receptorId = models.IntegerField(null=True)
    receptor = models.CharField(max_length=200, null=True)
    respuesta = models.CharField(max_length=200, null=True)
    respuestaAdjunto = models.CharField(max_length=255, null=True)


    fkusuario = models.ForeignKey(User, on_delete=models.CASCADE)

    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    fkusuarioEliminado = models.IntegerField(null=True)
    fechaEliminado = models.DateTimeField(null=True)

    class Meta:
        db_table = "system_chat"