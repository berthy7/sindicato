from django.shortcuts import render
from django.http import JsonResponse
from .models import Linea,Interno
from django.contrib.auth.decorators import login_required
import json
import datetime

# Create your views here.
@login_required
def index(request):
    return render(request, 'linea/index.html')

@login_required
def list(request):
    dt_list = []
    datos = Linea.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        internos = Interno.objects.filter(habilitado=True).count()
        dt_list.append(dict(id=item.id,codigo=item.codigo,
                            razonSocial=item.razonSocial,fechaFundacion=item.fechaFundacion.strftime('%d/%m/%Y'),nroAutorizacion=item.nroAutorizacion,
                            descripcionRuta=item.descripcionRuta,internos=internos,estado=item.estado))


    return JsonResponse(dt_list, safe=False)


@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        dicc['fechaFundacion'] = datetime.datetime.strptime(dicc['fechaFundacion'], '%d/%m/%Y')
        linea = Linea.objects.create(**dicc)
        for i in range(int(linea.internos)):
            nro = i + 1
            Interno.objects.create(numero=int(nro), fklinea=linea)

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']

        dicc['fechaFundacion'] = datetime.datetime.strptime(dicc['fechaFundacion'],'%d/%m/%Y')
        Linea.objects.filter(pk=dicc["id"]).update(**dicc)

        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)

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


@login_required
def agregarInternos(request):
    try:
        dicc = json.load(request)['obj']
        for i in range(int(dicc["internosAlguiler"])):
            nro = int(dicc["internos"]) + i +  1
            Interno.objects.create(numero=int(nro), fklinea=Linea.objects.get(id=dicc["id"]),observacion="Alquiler")

        return JsonResponse(dict(success=True, mensaje="Agregados Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
