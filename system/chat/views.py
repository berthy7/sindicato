from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.conf import settings as django_settings
from .models import Chat
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from system.linea.models import Linea,LineaPersona,Interno,InternoPersona
from system.incidente.models import Incidente
from system.persona.models import Persona
import json
import datetime
import os.path
import uuid
import io

# Create your views here.

@login_required
def home(request):
    user = request.user
    dt_list = []
    cumpleaños_list = []
    licencias_list = []
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona[0].fklinea:
            # datos = Chat.objects.filter(habilitado=True).filter(fkemisor=persona[0].fklinea).all().order_by('-id')
            datos = Chat.objects.filter(habilitado=True).all().order_by('-id')
        else:
            datos = Chat.objects.filter(habilitado=True).all().order_by('-id')

        for item in datos:
            # .strftime('%d/%m/%Y')
            dicc = model_to_dict(item)
            dt_list.append(dicc)

        fechaActual = datetime.datetime.now().date()
        # cumpleaños
        for item in Persona.objects.filter(fechaNacimiento=fechaActual):
            # .strftime('%d/%m/%Y')
            dicc = model_to_dict(item)
            cumpleaños_list.append(dicc)

        fecha10dias = fechaActual + datetime.timedelta(days=10)

        # licencias
        for item in Persona.objects.filter(habilitado=True).filter(Q(licenciaFechaVencimiento__range=(fechaActual, fecha10dias)) | Q(licenciaFechaVencimiento__lt=fechaActual)):
            # .strftime('%d/%m/%Y')
            dicc = model_to_dict(item)

            dicc["licenciaFechaVencimiento"] =item.licenciaFechaVencimiento.strftime('%d/%m/%Y')
            licencias_list.append(dicc)


    except Exception as e:
        print(e)


    dicc = dict(chat=[],cumpleaños=cumpleaños_list,licencias=licencias_list)


    return JsonResponse(dicc, safe=False)


@login_required
def index(request):
    user = request.user
    try:
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
    return render(request, 'persona/index.html', {'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})
@login_required
def list(request):
    dt_list = []
    datos = Chat.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('-id')
    for item in datos:
        dicc = model_to_dict(item)
        dt_list.append(dicc)
    return JsonResponse(dt_list, safe=False)

@login_required
def list(request):
    user = request.user
    dt_list = []
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona[0].fklinea:
            datos = Chat.objects.filter(habilitado=True).filter(fkemisor=persona[0].fklinea).all().order_by('-id')
        else:
            datos = Chat.objects.filter(habilitado=True).all().order_by('-id')

        for item in datos:
            # .strftime('%d/%m/%Y')
            dicc = model_to_dict(item)
            dt_list.append(dicc)

    except Exception as e:
        print(e)
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

        # interno = interPersona.fkinterno
        #
        # asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
        #                          fkinterno=interno.id, interno=interno.numero))
        asignacion = model_to_dict(interPersona)

        asignacion["interPersonaId"] = interPersona.id
        asignacion["linea"] = interPersona.fklinea.codigo if interPersona.fklinea else '---'
        asignacion["interno"] = interPersona.fkinterno.numero if interPersona.fkinterno else '---'
        asignaciones.append(asignacion)

    dicc = model_to_dict(persona)
    response = dict(obj=dicc,referencias=referencias,asignaciones=asignaciones)

    return JsonResponse(response, safe=False)
def handle_uploaded_file(f,name):
    with open('static/upload/'+ name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@login_required
def insert(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('foto', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            dicc["obj"]['foto'] = cname

        fileinfo = files.get('file-ci', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            dicc["obj"]['fotoCi'] = cname

        fileinfo = files.get('file-licencia', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['fotoLicencia'] = cname

        # dicc = json.load(request)['obj']
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
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('foto', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc['foto'] = cname

        fileinfo = files.get('file-ci', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc['fotoCi'] = cname

        fileinfo = files.get('file-licencia', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc['fotoLicencia'] = cname


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