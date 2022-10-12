from django.db import models
from django.contrib.auth.models import User
from system.persona.models import Persona
# Create your models here.



# class Evento(models.Model):
#     descripcion = models.CharField(max_length=25)
#     fechaIncidente = models.DateTimeField(null=True)
#     fkpersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
#
#     asociacion = models.CharField(max_length=25)
#     tipo = models.CharField(max_length=25)
#
#     fkusuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     fechar = models.DateTimeField(auto_now_add=True)
#     estado = models.BooleanField(default=True)
#     habilitado = models.BooleanField(default=True)
#
#     class Meta:
#         db_table = "system_evento"
