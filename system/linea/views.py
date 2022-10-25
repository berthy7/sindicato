from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Linea,Interno
from django.contrib.auth.decorators import login_required
import json
from system.persona.models import Persona
from system.linea.models import Linea,InternoPersona
from datetime import datetime

# Create your views here.
@login_required
def index(request):

    user = request.user
    try:
        # persona = get_object_or_404(Persona, fkusuario=user.id)
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
        else:
            lineaUser = ""

    except Exception as e:
        print(e)

    return render(request, 'linea/index.html', { 'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})



@login_required
def list(request):
    user = request.user
    dt_list = []
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona[0].fklinea:
            datos = Linea.objects.filter(habilitado=True).filter(id=persona[0].fklinea).all().order_by('-id')
        else:
            datos = Linea.objects.filter(habilitado=True).all().order_by('-id')

        for item in datos:
            internos = Interno.objects.filter(habilitado=True).filter(fklinea=item.id).count()
            dt_list.append(dict(id=item.id,codigo=item.codigo,
                                razonSocial=item.razonSocial,fechaFundacion=item.fechaFundacion.strftime('%d/%m/%Y'),
                                nombre=item.nombre, apellidos=item.apellidos,celular=item.celular,
                                ubicacion=item.ubicacion,internos=internos,estado=item.estado))
    except Exception as e:
        print(e)
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

@login_required
def listarInternosXLineaNoVehiculo(request,id):
    dt_list = []
    datos = Interno.objects.filter(habilitado=True).filter(fkvehiculo=None).filter(fklinea=int(id)).all().order_by('numero')
    for item in datos:
        dt_list.append(dict(id=item.id, numero=item.numero))

    return JsonResponse(dt_list, safe=False)


@login_required
def listarTodoInternosXLinea(request,id):
    dt_list = []
    datos = Interno.objects.filter(habilitado=True).filter(fklinea=int(id)).all().order_by('numero')
    for item in datos:
        dt_list.append(dict(id=item.id, numero=item.numero))

    return JsonResponse(dt_list, safe=False)


