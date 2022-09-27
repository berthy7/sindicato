from django.shortcuts import render
from django.http import JsonResponse
from .models import Vehiculo
from vehiculoCategoria.models import VehiculoCategoria
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def index(request):
    return render(request, 'bitacora/index.html')


@login_required
def list(request):

    dt_list = []
    datos = Vehiculo.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,placa=item.placa,
                            modelo=item.modelo,tipo=item.tipo,año=item.año, categoria = item.fkcategoria.nombre, estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']

        obj = VehiculoCategoria.objects.get(id=dicc["fkcategoria"])

        Vehiculo.objects.create(placa=dicc["placa"],modelo=dicc["modelo"],tipo=dicc["tipo"],año=dicc["año"],fkcategoria=obj)
        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        obj = Vehiculo.objects.get(id=dicc["id"])
        objVehiculoCategoria = VehiculoCategoria.objects.get(id=dicc["fkcategoria"])

        obj.placa =dicc["placa"]
        obj.modelo=dicc["modelo"]
        obj.tipo=dicc["tipo"]
        obj.año=dicc["año"]
        obj.fkcategoria = objVehiculoCategoria
        obj.save()
        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def state(request):
    try:
        dicc = json.load(request)['obj']
        obj = Vehiculo.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Vehiculo.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
