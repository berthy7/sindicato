from django.shortcuts import render
from django.http import JsonResponse
from .models import Incidente
from django.contrib.auth.decorators import login_required
from system.persona.models import Persona
import json

# Create your views here.
@login_required
def index(request):
    personas = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('nombre')

    return render(request, 'incidente/index.html', {'personas':personas})

@login_required
def list(request):
    dt_list = []
    datos = Incidente.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,nroIncidente=item.nroIncidente,
                            fechaIncidente=item.fechaIncidente, persona = item.fkpersona.nombre + " " + item.fkpersona.apellidos, fkpersona = item.fkpersona.id,
                            codigoUnidad=item.codigoUnidad,clasificacion=item.clasificacion,
                            descripcion=item.descripcion, acciones=item.acciones,
                            costo=item.costo,estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']
        dicc["fkpersona"] = Persona.objects.get(id=dicc["fkpersona"])
        dicc["fkusuario"] = user
        linea = Incidente.objects.create(**dicc)

        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        obj = Incidente.objects.get(id=dicc["id"])
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
        obj = Incidente.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Incidente.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
