from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Incidente,IncidenteTipo
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
        tipos = IncidenteTipo.objects.filter(habilitado=True).order_by('id')
        personas = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('nombre')
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineas = Linea.objects.filter(id=linea.id).all().order_by('id')
            lineaUser = linea.codigo
        else:
            rol = "Administrador"
            lineas = Linea.objects.all().order_by('id')
            lineaUser = ""
    except Exception as e:
        print(e)
    return render(request, 'incidente/index.html', {'personas': personas,'tipos': tipos,'lineas':lineas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})


@login_required
def list(request):
    dt_list = []
    datos = Incidente.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:


        dt_list.append(dict(id=item.id,fecha=item.fecha.strftime('%d/%m/%Y'),fktipo=item.fktipo.id,
                            responsable = item.responsable,otro=item.otro,fklinea=item.fklinea.id,
                            descripcion=item.descripcion,estados=item.estados,
                            costo=item.costo,estado=item.estado))
    return JsonResponse(dt_list, safe=False)
@login_required
def insert(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']

        dicc["fkpersona"] = Persona.objects.get(id=dicc["fkpersona"]) if dicc["fkpersona"] != "" else None
        dicc["fklinea"] = Linea.objects.get(id=dicc["fklinea"])
        dicc["fktipo"] = IncidenteTipo.objects.get(id=dicc["fktipo"])
        dicc["fkusuario"] = user
        dicc['fecha'] = datetime.datetime.strptime(dicc['fecha'], '%d/%m/%Y')

        if dicc["fkpersona"] != None:
            dicc["responsable"] = dicc["fkpersona"].nombre
        else:
            dicc["responsable"] = dicc["otro"]


        Incidente.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        dicc["fkpersona"] = Persona.objects.get(id=dicc["fkpersona"])
        dicc['fechaIncidente'] = datetime.datetime.strptime(dicc['fechaIncidente'],'%d/%m/%Y')
        Incidente.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
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


# Tipo
@login_required
def tipoList(request):
    dt_list = []
    datos = IncidenteTipo.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,nombre=item.nombre,estado=item.estado))
    return JsonResponse(dt_list, safe=False)
@login_required
def tipoInsert(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']
        dicc["fkusuario"] = user
        IncidenteTipo.objects.create(**dicc)
        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def tipoUpdate(request):
    try:
        dicc = json.load(request)['obj']
        IncidenteTipo.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def tipoState(request):
    try:
        dicc = json.load(request)['obj']
        obj = IncidenteTipo.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
@login_required
def tipoDelete(request):
    try:
        dicc = json.load(request)['obj']
        obj = IncidenteTipo.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)