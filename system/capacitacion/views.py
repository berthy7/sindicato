from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Capacitacion,CapacitacionCurso
from django.contrib.auth.decorators import login_required
from system.persona.models import Persona
from system.linea.models import Linea
from django.forms.models import model_to_dict
import json
import datetime

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        cursos = CapacitacionCurso.objects.filter(habilitado=True).order_by('id')
        personas = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('nombre')
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:

            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineas = Linea.objects.filter(id=linea.id).all().order_by('id')
            lineaUser = linea.codigo

        else:
            lineas = Linea.objects.all().order_by('id')
            lineaUser = ""


        foto = persona[0].foto if persona[0].foto != None else  ""

    except Exception as e:
        print(e)
    return render(request, 'capacitacion/index.html', {'personas': personas, 'cursos':cursos,'lineas':lineas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol,'foto': foto, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []

    user = request.user
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona[0].fklinea:
            datos = Capacitacion.objects.filter(habilitado=True).filter(fklinea=persona[0].fklinea).all().order_by('-id')
        else:
            datos = Capacitacion.objects.filter(habilitado=True).all().order_by('-id')

        for item in datos:
            dicc = model_to_dict(item)
            dicc["fecha"] = item.fecha.strftime('%d/%m/%Y')
            dicc["curso"] = item.fkcurso.nombre
            dicc["persona"] = item.fkpersona.nombre + " " + item.fkpersona.apellidos
            dicc["linea"] = item.fklinea.codigo

            dt_list.append(dicc)

    except Exception as e:
        print(e)

    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']
        dicc["fkcurso"] = CapacitacionCurso.objects.get(id=dicc["fkcurso"])
        dicc["fkpersona"] = Persona.objects.get(id=dicc["fkpersona"])
        dicc["fklinea"] = Linea.objects.get(id=dicc["fklinea"])
        dicc["fkusuario"] = user
        dicc['fecha'] = datetime.datetime.strptime(dicc['fecha'], '%d/%m/%Y')
        Capacitacion.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def update(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']
        dicc["fkcurso"] = CapacitacionCurso.objects.get(id=dicc["fkcurso"])
        dicc["fkpersona"] = Persona.objects.get(id=dicc["fkpersona"])
        dicc["fklinea"] = Linea.objects.get(id=dicc["fklinea"])
        dicc["fkusuario"] = user
        dicc['fecha'] = datetime.datetime.strptime(dicc['fecha'], '%d/%m/%Y')
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
    user = request.user
    try:
        dicc = json.load(request)['obj']
        obj = Capacitacion.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False

        obj.fechaEliminado = datetime.datetime.now() - datetime.timedelta(hours=4)
        obj.fkusuarioEliminado= user.id


        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)



# Curso
@login_required
def cursoList(request):
    dt_list = []
    datos = CapacitacionCurso.objects.filter(habilitado=True).all().order_by('id')
    for item in datos:
        dt_list.append(dict(id=item.id,nombre=item.nombre,estado=item.estado))
    return JsonResponse(dt_list, safe=False)
@login_required
def cursoInsert(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']
        dicc["fkusuario"] = user
        CapacitacionCurso.objects.create(**dicc)
        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", curso="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", curso="error"), safe=False)
@login_required
def cursoUpdate(request):
    try:
        dicc = json.load(request)['obj']
        CapacitacionCurso.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", curso="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", curso="error"), safe=False)
@login_required
def cursoState(request):
    try:
        dicc = json.load(request)['obj']
        obj = CapacitacionCurso.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
@login_required
def cursoDelete(request):
    try:
        dicc = json.load(request)['obj']
        obj = CapacitacionCurso.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)