from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from system.persona.models import Persona
from system.linea.models import Linea
from system.vehiculo.models import Vehiculo,VehiculoTransferencia
from system.capacitacion.models import Capacitacion
from system.incidente.models import Incidente
from django.db.models import Q

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        usuarios = User.objects.filter(is_active=True).filter(is_superuser=False).order_by('first_name')
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
        else:
            lineaUser = ""
        foto = persona[0].foto if persona[0].foto != None else  ""
    except Exception as e:
        print(e)
    return render(request, 'bitacora/index.html', {'usuario': user.first_name + " " + user.last_name,
                                             'usuarios': usuarios,'rol': rol,'foto': foto, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    dicc = json.load(request)['obj']
    try:

        if(dicc["opcion"] == "Linea"):
            dt_list = listar_lineas(dicc["usuario"])

        elif(dicc["opcion"] == "Socios"):
            dt_list = listar_socios(dicc["usuario"])

        elif (dicc["opcion"] == "Vehiculos"):
            dt_list = listar_vehiculos(dicc["usuario"])


        elif (dicc["opcion"] == "Conductores"):
            dt_list = listar_conductores(dicc["usuario"])


        elif (dicc["opcion"] == "Incidentes"):
            dt_list = listar_incidentes(dicc["usuario"])

        elif (dicc["opcion"] == "Capacitaciones"):
            dt_list = listar_capacitaciones(dicc["usuario"])



        return JsonResponse(dict(response=dt_list,success=True, mensaje="listado Correctamente", tipo="success"), safe=False)

    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)


def listar_vehiculos(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Vehiculo.objects.filter(Q(fkusuario=int(usuario)) | Q(fkusuarioEliminado=int(usuario))).all().order_by('-id')
    else:
        datos = Vehiculo.objects.all().order_by('-id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i, fecha=item.fechar.strftime('%d/%m/%Y'),
                            registro="Vehiculo",
                            nombre=item.fkusuario.first_name + " " + item.fkusuario.last_name,
                            id=item.id, descripcion=item.placa,
                            usuarioEliminacion=item.fkusuarioEliminado if item.fkusuarioEliminado else '----',
                            fechaEliminacion=item.fechaEliminado.strftime(
                                '%d/%m/%Y') if item.fechaEliminado else '----'))
    return dt_list

def listar_conductores(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Persona.objects.filter(tipo="Conductor").filter(Q(fkusuarioCreacion_id=int(usuario)) | Q(fkusuarioEliminado=int(usuario))).all().order_by('id')
    else:
        datos = Persona.objects.filter(tipo="Conductor").all().order_by('id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i, fecha=item.fechar.strftime('%d/%m/%Y'),
                            registro="Conductor",
                            nombre=item.fkusuarioCreacion.first_name + " " + item.fkusuarioCreacion.last_name,
                            id=item.id, descripcion=item.nombre + " " + item.apellidos,
                            usuarioEliminacion=item.fkusuarioEliminado if item.fkusuarioEliminado else '----',
                            fechaEliminacion=item.fechaEliminado.strftime(
                                '%d/%m/%Y') if item.fechaEliminado else '----'))
    return dt_list

def listar_lineas(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Linea.objects.filter(Q(fkusuario_id=int(usuario)) | Q(fkusuarioEliminado=int(usuario))).all().order_by('id')
    else:
        datos = Linea.objects.all().order_by('id')

    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i, fecha=item.fechar.strftime('%d/%m/%Y'),
                            registro="Linea",
                            nombre=item.fkusuario.first_name + " " + item.fkusuario.last_name,
                            id=item.id, descripcion=item.codigo,
                            usuarioEliminacion=item.fkusuarioEliminado if item.fkusuarioEliminado else '----',
                            fechaEliminacion=item.fechaEliminado.strftime(
                                '%d/%m/%Y') if item.fechaEliminado else '----'))
    return dt_list

def listar_socios(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Persona.objects.filter(tipo="Socio").filter(Q(fkusuarioCreacion_id=int(usuario)) | Q(fkusuarioEliminado=int(usuario))).all().order_by('-id')
    else:
        datos = Persona.objects.filter(tipo="Socio").all().order_by('-id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i, fecha=item.fechar.strftime('%d/%m/%Y'),
                            registro="Socio",
                            nombre=item.fkusuarioCreacion.first_name + " " + item.fkusuarioCreacion.last_name,
                            id=item.id, descripcion=item.nombre + " " + item.apellidos,
                            usuarioEliminacion=item.fkusuarioEliminado if item.fkusuarioEliminado else '----',
                            fechaEliminacion=item.fechaEliminado.strftime(
                                '%d/%m/%Y') if item.fechaEliminado else '----'))
    return dt_list

def listar_incidentes(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Incidente.objects.filter(Q(fkusuario_id=int(usuario)) | Q(fkusuarioEliminado=int(usuario))).all().order_by('-id')
    else:
        datos = Incidente.objects.all().order_by('-id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i,fecha=item.fechar.strftime('%d/%m/%Y'),
                            registro = "Incidente",
                            nombre=item.fkusuario.first_name + " " +item.fkusuario.last_name,
                            id=item.id,descripcion=item.descripcion,
                            usuarioEliminacion=item.fkusuarioEliminado.first_name + " " +item.fkusuario.last_name if item.fkusuarioEliminado else '----',
                            fechaEliminacion=item.fechaEliminado.strftime('%d/%m/%Y')  if item.fechaEliminado else '----'))
    return dt_list

def listar_capacitaciones(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Capacitacion.objects.filter(Q(fkusuario_id=int(usuario)) | Q(fkusuarioEliminado=int(usuario))).all().order_by('-id')
    else:
        datos = Capacitacion.objects.all().order_by('-id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i,fecha=item.fechar.strftime('%d/%m/%Y'),
                            registro = "Capacitacion",
                            nombre=item.fkusuario.first_name + " " +item.fkusuario.last_name,
                            id=item.id,descripcion=item.descripcion,
                            usuarioEliminacion=item.fkusuarioEliminado.first_name + " " +item.fkusuario.last_name if item.fkusuarioEliminado else '----',
                            fechaEliminacion=item.fechaEliminado.strftime('%d/%m/%Y')  if item.fechaEliminado else '----'))
    return dt_list