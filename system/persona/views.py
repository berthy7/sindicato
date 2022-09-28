from django.shortcuts import render
from django.http import JsonResponse
from .models import Persona
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def index(request):
    return render(request, 'persona/index.html')

@login_required
def list(request):
    dt_list = []
    datos = Persona.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,tipo=item.tipo,ci=item.ci,nombre=item.nombre,apellidos=item.apellidos,domicilio=item.domicilio,estado=item.estado))

    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']

        Persona.objects.create(ci=dicc["ci"],nombre=dicc["nombre"],apellidos=dicc["apellidos"],
                               genero=dicc["genero"],licenciaNro=dicc["licenciaNro"],licenciaCategoria=dicc["licenciaCategoria"],
                               licenciaFechaVencimiento=dicc["licenciaFechaVencimiento"], lugarNacimiento=dicc["lugarNacimiento"],
                               domicilio=dicc["domicilio"],tipo=dicc["tipo"])
        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        obj = Persona.objects.get(id=dicc["id"])
        obj.codigo =dicc["codigo"]
        obj.razonSocial=dicc["razonSocial"]
        obj.denominacion=dicc["denominacion"]
        obj.nroAutorizacion=dicc["nroAutorizacion"]
        obj.descripcionRuta = dicc["descripcionRuta"]
        obj.fechaFundacion = dicc["fechaFundacion"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def state(request):
    try:
        dicc = json.load(request)['obj']
        obj = Persona.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Persona.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
