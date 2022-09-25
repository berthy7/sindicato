from django.db import models

# Create your models here.


class Conductor(models.Model):

    ci = models.CharField(max_length=25)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "conductor"