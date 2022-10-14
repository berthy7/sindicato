from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Persona, PersonaReferencia
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
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
    return render(request, 'persona/index.html', {'personas': personas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})


@login_required
def list(request):
    dt_list = []
    datos = Persona.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,tipo=item.tipo,ci=item.ci,
                            nombre=item.nombre,apellidos=item.apellidos,
                            domicilio=item.domicilio,estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def obtain(request,id):

    persona = Persona.objects.get(id=id)
    persona.ciFechaVencimiento = persona.ciFechaVencimiento.strftime('%d/%m/%Y')
    persona.licenciaFechaVencimiento = persona.licenciaFechaVencimiento.strftime('%d/%m/%Y')
    referencias = []

    for ref in PersonaReferencia.objects.filter(fkpersona=persona.id).all().order_by('id'):
        referencias.append(model_to_dict(ref))

    dicc = model_to_dict(persona)
    response = dict(obj=dicc,referencias=referencias)

    return JsonResponse(response, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['response']
        dicc["obj"]['ciFechaVencimiento'] = datetime.datetime.strptime(dicc["obj"]['ciFechaVencimiento'],'%d/%m/%Y')
        dicc["obj"]['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc["obj"]['licenciaFechaVencimiento'], '%d/%m/%Y')
        persona = Persona.objects.create(**dicc["obj"])

        for ref in dicc["referencias"]:
            ref["fkpersona"] =  persona
            PersonaReferencia.objects.create(**ref)

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']

        dicc['ciFechaVencimiento'] = datetime.datetime.strptime(dicc['ciFechaVencimiento'],'%d/%m/%Y')
        dicc['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc['licenciaFechaVencimiento'], '%d/%m/%Y')

        Persona.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

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


@login_required
def listarPersonaXTipo(request,id):

    dt_list = []
    datos = Persona.objects.filter(habilitado=True).filter(tipo=id).all().order_by('nombre')
    for item in datos:
        dt_list.append(dict(id=item.id, nombre=item.nombre + " " + item.apellidos))

    return JsonResponse(dt_list, safe=False)
