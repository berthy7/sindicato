from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Capacitacion
from django.contrib.auth.decorators import login_required
from system.persona.models import Persona
from system.linea.models import Linea
import json
import datetime

# Create your views here.
@login_required
def index(request):

    user = request.user
    try:
        # persona = get_object_or_404(Persona, fkusuario=user.id)
        personas = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('nombre')
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:

            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
        else:
            rol = "Administrador"
            lineaUser = ""
    except Exception as e:
        print(e)
    return render(request, 'capacitacion/index.html', {'personas': personas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})


@login_required
def list(request):
    dt_list = []
    datos = Capacitacion.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,nroCapacitacion=item.nroCapacitacion,
                            fechaCapacitacion=item.fechaCapacitacion.strftime('%d/%m/%Y'), persona = item.fkpersona.nombre + " " + item.fkpersona.apellidos, fkpersona = item.fkpersona.id,
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
        dicc['fechaCapacitacion'] = datetime.datetime.strptime(dicc['fechaCapacitacion'], '%d/%m/%Y')
        Capacitacion.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        dicc["fkpersona"] = Persona.objects.get(id=dicc["fkpersona"])
        dicc['fechaCapacitacion'] = datetime.datetime.strptime(dicc['fechaCapacitacion'],'%d/%m/%Y')
        Capacitacion.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def state(request):
    try:
        dicc = json.load(request)['obj']
        obj = Capacitacion.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Capacitacion.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
