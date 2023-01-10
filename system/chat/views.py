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
from system.vehiculo.models import Vehiculo
import json
import datetime

import os.path
import uuid
import io
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.

@login_required
def home(request):
    user = request.user
    dt_list = []
    cumpleaños_list = []
    licencias_list = []
    vehiculo_list = []
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        fechaActual = datetime.datetime.now().date()
        fecha10dias = fechaActual + datetime.timedelta(days=10)
        if persona[0].fklinea:

            datos = Chat.objects.filter(habilitado=True).filter(Q(emisorId=user.id) | Q(receptorId=user.id)).all().order_by('-id')

            for item in datos:
                dicc = model_to_dict(item)

                dicc["fecha"] = item.fecha.strftime('%d/%m/%Y %H:%M')

                if dicc["fechar"] != None:
                    dicc["fechar"] = item.fechar.strftime('%d/%m/%Y %H:%M')
                else:
                    dicc["fechar"] = ""

                dt_list.append(dicc)

            # cumpleaños
            for interPer in InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct(
                    'fkpersona').all().select_related('fkpersona').filter(fkpersona__fechaNacimiento=fechaActual).filter(
                    fkpersona__habilitado=True):
                item = interPer.fkpersona
                dicc = model_to_dict(item)
                cumpleaños_list.append(dicc)
            # licencias

            for interPer in InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct(
                    'fkpersona').all().select_related('fkpersona').filter(fkpersona__habilitado=True).filter(
                Q(fkpersona__licenciaFechaVencimiento__range=(fechaActual, fecha10dias)) | Q(
                    fkpersona__licenciaFechaVencimiento__lt=fechaActual)):
                item = interPer.fkpersona
                dicc = model_to_dict(item)
                dicc["licenciaFechaVencimiento"] = item.licenciaFechaVencimiento.strftime('%d/%m/%Y')
                licencias_list.append(dicc)

            # vehiculos
            # soat
            for vehiculo in Vehiculo.objects.filter(fklinea=persona[0].fklinea).filter(habilitado=True).filter(
                        Q(soatVencimiento__range=(fechaActual, fecha10dias)) | Q(
                        soatVencimiento__lt=fechaActual)):

                dicc = model_to_dict(vehiculo)
                dicc["fecha"] = vehiculo.soatVencimiento.strftime('%d/%m/%Y')
                dicc["documento"] = "Soat"
                vehiculo_list.append(dicc)

            # inspeccion
            for vehiculo in Vehiculo.objects.filter(fklinea=persona[0].fklinea).filter(habilitado=True).filter(
                            Q(inspeccionVencimiento__range=(fechaActual, fecha10dias)) | Q(
                        inspeccionVencimiento__lt=fechaActual)):
                dicc = model_to_dict(vehiculo)
                dicc["fecha"] = vehiculo.inspeccionVencimiento.strftime('%d/%m/%Y')
                dicc["documento"] = "Inspección Técnica"
                vehiculo_list.append(dicc)

            # seguro
            for vehiculo in Vehiculo.objects.filter(fklinea=persona[0].fklinea).filter(habilitado=True).filter(
                            Q(seguroVencimiento__range=(fechaActual, fecha10dias)) | Q(
                        seguroVencimiento__lt=fechaActual)):
                dicc = model_to_dict(vehiculo)
                dicc["fecha"] = vehiculo.seguroVencimiento.strftime('%d/%m/%Y')
                dicc["documento"] = "Seguro"
                vehiculo_list.append(dicc)


        else:
            datos = Chat.objects.filter(habilitado=True).all().order_by('-id')
            for item in datos:
                dicc = model_to_dict(item)
                dicc["fecha"] = item.fecha.strftime('%d/%m/%Y %H:%M')

                if dicc["fechar"] != None:
                    dicc["fechar"] = item.fechar.strftime('%d/%m/%Y %H:%M')
                else:
                    dicc["fechar"] = ""

                dt_list.append(dicc)
            # cumpleaños
            for item in Persona.objects.filter(habilitado=True).filter(fechaNacimiento=fechaActual):
                dicc = model_to_dict(item)
                cumpleaños_list.append(dicc)
            # licencias
            for item in Persona.objects.filter(habilitado=True).filter(
                Q(licenciaFechaVencimiento__range=(fechaActual, fecha10dias)) | Q(
                    licenciaFechaVencimiento__lt=fechaActual)):
                # .strftime('%d/%m/%Y')
                dicc = model_to_dict(item)
                dicc["licenciaFechaVencimiento"] = item.licenciaFechaVencimiento.strftime('%d/%m/%Y')
                licencias_list.append(dicc)

            # vehiculos
            # soat
            for vehiculo in Vehiculo.objects.filter(habilitado=True).filter(
                        Q(soatVencimiento__range=(fechaActual, fecha10dias)) | Q(
                        soatVencimiento__lt=fechaActual)):

                dicc = model_to_dict(vehiculo)
                dicc["fecha"] = vehiculo.soatVencimiento.strftime('%d/%m/%Y')
                dicc["documento"] = "Soat"
                vehiculo_list.append(dicc)

            # inspeccion
            for vehiculo in Vehiculo.objects.filter(habilitado=True).filter(
                            Q(inspeccionVencimiento__range=(fechaActual, fecha10dias)) | Q(
                        inspeccionVencimiento__lt=fechaActual)):
                dicc = model_to_dict(vehiculo)
                dicc["fecha"] = vehiculo.inspeccionVencimiento.strftime('%d/%m/%Y')
                dicc["documento"] = "Inspección Técnica"
                vehiculo_list.append(dicc)

            # seguro
            for vehiculo in Vehiculo.objects.filter(habilitado=True).filter(
                            Q(seguroVencimiento__range=(fechaActual, fecha10dias)) | Q(
                        seguroVencimiento__lt=fechaActual)):
                dicc = model_to_dict(vehiculo)
                dicc["fecha"] = vehiculo.seguroVencimiento.strftime('%d/%m/%Y')
                dicc["documento"] = "Seguro"
                vehiculo_list.append(dicc)
    except Exception as e:
        print(e)

    dicc = dict(userid=user.id, chat=dt_list,cumpleaños=cumpleaños_list,licencias=licencias_list,vehiculos=vehiculo_list)
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
            lineaUser = ""

        foto = persona[0].foto if persona[0].foto != None else  ""
    except Exception as e:
        print(e)
    return render(request, 'persona/index.html', {'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'foto': foto,'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    user = request.user
    admin = False
    persona = Persona.objects.filter(fkusuario=user.id)
    if persona[0].fklinea:
        admin = False
        for interPer in  InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct('fkpersona').all().select_related('fkpersona').filter(fkpersona__tipo='Socio').filter(fkpersona__habilitado=True):
            item = interPer.fkpersona
            asignaciones = []
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(
                    fkpersona=item.id).all().order_by('id'):
                interno = interPersona.fkinterno
                asignaciones.append(
                    dict(interPersonaId=interPersona.id, fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                         fkinterno=interno.id, interno=interno.numero))
            dicc = model_to_dict(item)
            dicc["asignaciones"] = asignaciones
            dt_list.append(dicc)

        obj = dict(admin=admin, lista=dt_list)
        return JsonResponse(obj, safe=False)
    else:
        datos = Persona.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('-id')
        admin = True
        for item in datos:
            asignaciones = []
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
                interno = interPersona.fkinterno
                asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                                         fkinterno=interno.id, interno=interno.numero))
            dicc = model_to_dict(item)
            dicc["asignaciones"] = asignaciones
            dt_list.append(dicc)

        obj = dict(admin=admin, lista=dt_list)
        return JsonResponse(obj, safe=False)

@login_required
def obtain(request,id):
    persona = Persona.objects.get(id=id)
    if persona.fechaNacimiento:
        persona.fechaNacimiento = persona.fechaNacimiento.strftime('%d/%m/%Y')
    if persona.licenciaFechaVencimiento:
        persona.licenciaFechaVencimiento = persona.licenciaFechaVencimiento.strftime('%d/%m/%Y')
    if persona.fechaInscripcion:
        persona.fechaInscripcion = persona.fechaInscripcion.strftime('%d/%m/%Y')

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

def upload_cloudinay(foto):
    resp= cloudinary.uploader.upload('static/upload/'+foto)
    return resp["secure_url"]

def handle_uploaded_file(f,name):
    with open('static/upload/'+ name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@login_required
def insert(request):
    user = request.user
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('file', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            dicc['mensajeAdjunto'] = upload_cloudinay(cname)

        dicc['fkusuario'] = user

        Chat.objects.create(**dicc)
        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)

    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def update(request):
    user = request.user
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('file', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            dicc['mensajeAdjunto'] = upload_cloudinay(cname)

        dicc['receptorId'] = user.id
        dicc['receptor'] = user.first_name + " " + user.last_name

        dicc['fechar'] = datetime.datetime.now() - datetime.timedelta(hours=4)

        Chat.objects.filter(pk=dicc["id"]).update(**dicc)
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
def delete(request,id):
    user = request.user
    try:
        obj = Chat.objects.get(id=id)
        obj.estado = False
        obj.habilitado = False

        obj.fechaEliminado = datetime.datetime.now() - datetime.timedelta(hours=4)
        obj.fkusuarioEliminado= user.id

        obj.save()

        dt_list = []
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona[0].fklinea:
            datos = Chat.objects.filter(habilitado=True).filter(
                Q(emisorId=user.id) | Q(receptorId=user.id)).all().order_by('-id')

            for item in datos:
                dicc = model_to_dict(item)

                dicc["fecha"] = item.fecha.strftime('%d/%m/%Y %H:%M')

                if dicc["fechar"] != None:
                    dicc["fechar"] = item.fechar.strftime('%d/%m/%Y %H:%M')
                else:
                    dicc["fechar"] = ""

                dt_list.append(dicc)

        else:
            datos = Chat.objects.filter(habilitado=True).all().order_by('-id')
            for item in datos:
                dicc = model_to_dict(item)
                dicc["fecha"] = item.fecha.strftime('%d/%m/%Y %H:%M')

                if dicc["fechar"] != None:
                    dicc["fechar"] = item.fechar.strftime('%d/%m/%Y %H:%M')
                else:
                    dicc["fechar"] = ""

                dt_list.append(dicc)

        req = dict(userid=user.id, chat=dt_list)

        return JsonResponse(dict(success=True, response=req, mensaje="Eliminado Correctamente", tipo="success"), safe=False)

    except Exception as e:
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)