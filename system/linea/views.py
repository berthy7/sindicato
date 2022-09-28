from django.shortcuts import render
from django.http import JsonResponse
from .models import Linea
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def index(request):
    return render(request, 'linea/index.html')

@login_required
def list(request):
    dt_list = []
    datos = Linea.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,codigo=item.codigo,
                            razonSocial=item.razonSocial,denominacion=item.denominacion,
                            fechaFundacion=item.fechaFundacion,nroAutorizacion=item.nroAutorizacion,
                            descripcionRuta=item.descripcionRuta,estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        Linea.objects.create(codigo=dicc["codigo"],razonSocial=dicc["razonSocial"],denominacion=dicc["denominacion"],
                             nroAutorizacion=dicc["nroAutorizacion"], descripcionRuta=dicc["descripcionRuta"],fechaFundacion=dicc["fechaFundacion"])
        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        obj = Linea.objects.get(id=dicc["id"])
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
        obj = Linea.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Linea.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)