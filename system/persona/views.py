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


        dt_list.append(model_to_dict(item))

        # dt_list.append(dict(id=item.id,tipo=item.tipo,ci=item.ci,
        #                     nombre=item.nombre,apellidos=item.apellidos,
        #                     domicilio=item.domicilio,estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def obtain(request,id):

    persona = Persona.objects.get(id=id)

    if persona.ciFechaVencimiento:
        persona.ciFechaVencimiento = persona.ciFechaVencimiento.strftime('%d/%m/%Y')
    if persona.licenciaFechaVencimiento:
        persona.licenciaFechaVencimiento = persona.licenciaFechaVencimiento.strftime('%d/%m/%Y')

    referencias = []

    for ref in PersonaReferencia.objects.filter(fkpersona=persona.id).all().order_by('id'):
        referencias.append(model_to_dict(ref))

    asignaciones = []

    for lin in LineaPersona.objects.filter(fkpersona=persona.id).all().order_by('id'):
        asignaciones.append(dict(fklinea=lin.fklinea.id,linea=lin.fklinea.codigo,fkinterno="",interno=""))

    for inter in InternoPersona.objects.filter(fkpersona=persona.id).all().order_by('id'):
        linea = Linea.objects.get(id=inter.fkinterno.fklinea.id)
        asignaciones.append(dict(fklinea=linea.id,linea=linea.codigo,fkinterno=inter.fkinterno.id,interno=inter.fkinterno.numero))


    dicc = model_to_dict(persona)
    response = dict(obj=dicc,referencias=referencias,asignaciones=asignaciones)

    return JsonResponse(response, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['response']

        persona = Persona.objects.filter(ci=dicc["obj"]['ci']).all()

        if len(persona) == 0:
            if dicc["obj"]['ciFechaVencimiento'] != "":
                dicc["obj"]['ciFechaVencimiento'] = datetime.datetime.strptime(dicc["obj"]['ciFechaVencimiento'],'%d/%m/%Y')
            else:
                dicc["obj"]['ciFechaVencimiento'] = None

            if dicc["obj"]['licenciaFechaVencimiento'] != "":
                dicc["obj"]['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc["obj"]['licenciaFechaVencimiento'],'%d/%m/%Y')
            else:
                dicc["obj"]['licenciaFechaVencimiento'] = None

            persona = Persona.objects.create(**dicc["obj"])

            for ref in dicc["referencias"]:
                ref["fkpersona"] =  persona
                PersonaReferencia.objects.create(**ref)

            for asig in dicc["lineas"]:

                if asig["fkinterno"] != "":
                    asig["fkinterno"] =  Interno.objects.get(id=asig["fkinterno"])
                    asig["fkpersona"] = persona
                    del asig['fklinea']
                    del asig['linea']
                    del asig['interno']
                    InternoPersona.objects.create(**asig)
                else:
                    asig["fklinea"] =  Linea.objects.get(id=asig["fklinea"])
                    asig["fkpersona"] = persona
                    del asig['fkinterno']
                    del asig['linea']
                    del asig['interno']
                    LineaPersona.objects.create(**asig)

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
        if dicc['ciFechaVencimiento'] != "":
            dicc['ciFechaVencimiento'] = datetime.datetime.strptime(dicc['ciFechaVencimiento'],'%d/%m/%Y')
        else:
            dicc['ciFechaVencimiento'] = None
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
