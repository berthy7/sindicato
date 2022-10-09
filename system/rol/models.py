from django.db import models
from django.contrib.auth.models import Group

# Create your models here.

class Modulo(models.Model):
    titulo = models.CharField(max_length=50)
    url = models.CharField(max_length=50,null=True)
    nombre = models.CharField(max_length=50)
    icono = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20)
    orden = models.IntegerField()
    fkmodulo = models.ForeignKey('self', on_delete=models.CASCADE,null=True)

    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "auth_modules"


class Permisos(models.Model):

    fkrol = models.ForeignKey(Group, on_delete=models.CASCADE)
    fkmodulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    class Meta:
        db_table = "auth_permisos"