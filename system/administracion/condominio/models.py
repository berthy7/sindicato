from django.db import models

# Create your models here.


class Condominio(models.Model):

    codigo = models.CharField(max_length=100)
    nombre = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)
    fechaRegistro = models.DateField(null=True)
    estado = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = "administracion_condominio"

