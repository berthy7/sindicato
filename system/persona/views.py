from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Persona, PersonaReferencia
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from system.linea.models import Linea,LineaPersona,Interno,InternoPersona
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
            lineas = Linea.objects.filter(habilitado=True).filter(id=linea.id).all().order_by('id')
        else:
            rol = "Administrador"
            lineaUser = ""
            lineas = Linea.objects.filter(habilitado=True).all().order_by('id')
    except Exception as e:
        print(e)
    return render(request, 'persona/index.html', {'personas': personas,'lineas':lineas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    datos = Persona.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('-id')
    for item in datos:
        asignaciones = []
        for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
            interno = interPersona.fkinterno
            asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                                     fkinterno=interno.id, interno=interno.numero))


        dicc = model_to_dict(item)
        dicc["asignaciones"] = asignaciones
        dt_list.append(dicc)
    return JsonResponse(dt_list, safe=False)

@login_required
def obtain(request,id):

    persona = Persona.objects.get(id=id)

    if persona.fechaNacimiento:
        persona.fechaNacimiento = persona.fechaNacimiento.strftime('%d/%m/%Y')
    if persona.licenciaFechaVencimiento:
        persona.licenciaFechaVencimiento = persona.licenciaFechaVencimiento.strftime('%d/%m/%Y')

    referencias = []

    for ref in PersonaReferencia.objects.filter(habilitado=True).filter(fkpersona=persona.id).all().order_by('id'):
        referencias.append(model_to_dict(ref))

    asignaciones = []
    for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=persona.id).all().order_by('id'):
        interno = interPersona.fkinterno
        asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                                 fkinterno=interno.id, interno=interno.numero))

    dicc = model_to_dict(persona)
    response = dict(obj=dicc,referencias=referencias,asignaciones=asignaciones)

    return JsonResponse(response, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        persona = Persona.objects.filter(ci=dicc["obj"]['ci']).filter(habilitado=True).all()

        if len(persona) == 0:
            if dicc["obj"]['fechaNacimiento'] != "":
                dicc["obj"]['fechaNacimiento'] = datetime.datetime.strptime(dicc["obj"]['fechaNacimiento'],'%d/%m/%Y')
            else:
                dicc["obj"]['fechaNacimiento'] = None

            if dicc["obj"]['licenciaFechaVencimiento'] != "":
                dicc["obj"]['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc["obj"]['licenciaFechaVencimiento'],'%d/%m/%Y')
            else:
                dicc["obj"]['licenciaFechaVencimiento'] = None
            del dicc["obj"]['id']
            persona = Persona.objects.create(**dicc["obj"])

            for ref in dicc["referencias"]:
                del ref['id']
                ref["fkpersona"] =  persona
                PersonaReferencia.objects.create(**ref)

            for asig in dicc["lineas"]:
                asig["fkinterno"] =  Interno.objects.get(id=asig["fkinterno"])
                asig["fkpersona"] = persona
                del asig['interPersonaId']
                del asig['fklinea']
                del asig['linea']
                del asig['interno']

                InternoPersona.objects.create(**asig)

            return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
        else:
            return JsonResponse(dict(success=False, mensaje="El Ci ya esta registrado en el sistema", tipo="warning"), safe=False)

    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        if dicc['fechaNacimiento'] != "":
            dicc['fechaNacimiento'] = datetime.datetime.strptime(dicc['fechaNacimiento'],'%d/%m/%Y')
        else:
            dicc['fechaNacimiento'] = None
        if dicc['licenciaFechaVencimiento'] != "":
            dicc['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc['licenciaFechaVencimiento'], '%d/%m/%Y')
        else:
            dicc['licenciaFechaVencimiento'] = None

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
@login_required
def agregarInternos(request):
    try:
        dicc = json.load(request)['obj']

        del dicc['interPersonaId']
        del dicc['fklinea']
        del dicc['linea']
        del dicc['interno']

        dicc['fkinterno'] = Interno.objects.get(id=dicc["fkinterno"])
        dicc['fkpersona'] = Persona.objects.get(id=dicc["fkpersona"])
        InternoPersona.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Agregado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def eliminarInternos(request,id):
    try:
        interno = InternoPersona.objects.get(id=id)
        interno.estado = False
        interno.habilitado = False
        interno.fechaRetiro = datetime.datetime.now()
        interno.save()
        return JsonResponse(dict(success=True, mensaje="Eliminado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def eliminarReferencia(request,id):
    try:
        referencia = PersonaReferencia.objects.get(id=id)
        referencia.estado = False
        referencia.habilitado = False
        referencia.save()
        return JsonResponse(dict(success=True, mensaje="Eliminado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def agregarReferencia(request):
    try:
        dicc = json.load(request)['obj']
        dicc['fkpersona'] = Persona.objects.get(id=dicc["fkpersona"])
        del dicc['id']
        PersonaReferencia.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Agregado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def modificarReferencia(request):
    try:
        dicc = json.load(request)['obj']
        dicc['fkpersona'] = Persona.objects.get(id=dicc["fkpersona"])
        PersonaReferencia.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Actualizado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
