import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from system.vehiculoCategoria.models import VehiculoCategoria
from .models import Vehiculo
from system.linea.models import Linea,LineaVehiculo,Interno,LineaPersona,InternoVehiculo
from django.contrib.auth.models import User
from system.persona.models import Persona

import os.path
import uuid
import io
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            internos = Interno.objects.filter(fklinea=linea.id).filter(fkvehiculo = None ).all().order_by('id')
            lineas = Linea.objects.filter(habilitado=True).filter(id=linea.id).all().order_by('id')
            lineaUser = linea.codigo
        else:
            rol = "Administrador"
            internos = Interno.objects.filter(fkvehiculo = None ).all().order_by('id')
            lineas = Linea.objects.filter(habilitado=True).all().order_by('id')
            lineaUser = ""
        categorias = VehiculoCategoria.objects.all().order_by('id')
    except Exception as e:
        print(e)
    return render(request, 'vehiculo/index.html', {'categorias':categorias,
                                                   'lineas':lineas,'internos':internos,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})

@login_required
def list(request):
    user = request.user
    admin = False
    dt_list = []
    persona = Persona.objects.filter(fkusuario=user.id)

    if persona[0].fklinea:
        datos = Vehiculo.objects.filter(fklinea=persona[0].fklinea).filter(habilitado=True).all().order_by('-id')
        admin = False
    else:
        datos = Vehiculo.objects.filter(habilitado=True).all().order_by('-id')
        admin = True

    for item in datos:
        linId = 0
        lin = "Sin linea"
        if item.fklinea != None:
            linea = Linea.objects.get(id=item.fklinea)
            linId = linea.id
            lin = linea.codigo

        interId = 0
        inter = "Sin Interno"

        if item.fkinterno != None:
            interno = Interno.objects.get(id=item.fkinterno)
            interId = interno.id
            inter = interno.numero

        dt_list.append(dict(id=item.id,fklinea=linId,linea=lin,fkinterno=interId,interno=inter,placa=item.placa,ruat=item.ruat,frontal=item.fotofrontal,lateral=item.fotolateral,
                            modelo=item.modelo,tipo=item.tipo,año=item.año, categoria = item.fkcategoria.nombre, fkcategoria = item.fkcategoria.id, estado=item.estado))

    obj = dict(admin=admin, lista=dt_list)
    return JsonResponse(obj, safe=False)

def upload_cloudinay(foto):
    resp= cloudinary.uploader.upload('static/upload/'+foto)
    return resp["secure_url"]

def handle_uploaded_file(f,name):
    with open('static/upload/'+ name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def insertfile(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        obj = Vehiculo.objects.get(id=dicc['id'])
        files = request.FILES

        fileinfo = files.get('ruat', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            obj.ruat = upload_cloudinay(cname)

        fileinfo = files.get('frontal', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            obj.fotofrontal = upload_cloudinay(cname)

        fileinfo = files.get('lateral', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            obj.fotolateral = upload_cloudinay(cname)

        obj.save()
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)

@login_required
def insert(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('ruat', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['ruat'] = upload_cloudinay(cname)

        fileinfo = files.get('frontal', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['fotofrontal'] = upload_cloudinay(cname)

        fileinfo = files.get('lateral', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['fotolateral'] = upload_cloudinay(cname)

        dicc["obj"]["fkcategoria"] = VehiculoCategoria.objects.get(id=dicc["obj"]["fkcategoria"])
        del dicc["obj"]['id']
        vehiculo = Vehiculo.objects.create(**dicc["obj"])

        # registrar linea
        linea = Linea.objects.get(id=dicc["fklinea"])
        lineavehiculo = LineaVehiculo.objects.filter(estado=True) \
            .filter(fkvehiculo=vehiculo).all()
        if len(lineavehiculo) >0:
            lineavehiculo[0].estado = False
            lineavehiculo[0].save()
        LineaVehiculo.objects.create(**dict(fkvehiculo=vehiculo,fklinea=linea))

        # registrar interno
        interno = Interno.objects.get(id=dicc["fkinterno"])
        internoVehiculo = InternoVehiculo.objects.filter(estado=True) \
            .filter(fkvehiculo=vehiculo).all()
        if len(internoVehiculo) >0:
            internoVehiculo[0].estado = False
            internoVehiculo[0].save()

        interno.fkvehiculo = vehiculo
        interno.save()
        InternoVehiculo.objects.create(**dict(fkvehiculo=vehiculo,fkinterno=interno))

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def update(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('ruat', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['ruat'] = upload_cloudinay(cname)

        fileinfo = files.get('frontal', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['fotofrontal'] = upload_cloudinay(cname)

        fileinfo = files.get('lateral', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['fotolateral'] = upload_cloudinay(cname)

        dicc["obj"]['fkcategoria'] = VehiculoCategoria.objects.get(id=dicc["obj"]["fkcategoria"])
        Vehiculo.objects.filter(pk=dicc["obj"]["id"]).update(**dicc["obj"])

        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def state(request):
    try:
        dicc = json.load(request)['obj']
        obj = Vehiculo.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Vehiculo.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)



@login_required
def asignacion(request):
    try:

        dicc = json.load(request)['obj']
        vehiculo = Vehiculo.objects.get(id=dicc["fkvehiculo"])
        linea = Linea.objects.get(id=dicc["fklinea"])

        lineavehiculo = LineaVehiculo.objects.filter(estado=True) \
            .filter(fkvehiculo=vehiculo).all()

        if len(lineavehiculo) >0:
            lineavehiculo[0].estado = False
            lineavehiculo[0].save()

        LineaVehiculo.objects.create(**dict(fkvehiculo=vehiculo,fklinea=linea,fechaAsignacion=dicc["fechaAsignacion"]))

        return JsonResponse(dict(success=True,mensaje="Se asigno"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)



@login_required
def retiro(request):
    try:
        dicc = json.load(request)['obj']
        lineavehiculo = LineaVehiculo.objects.get(id=dicc["lineavehiculoid"])

        lineavehiculo.fechaRetiro = dicc["fechaRetiro"]
        lineavehiculo.estado = False

        lineavehiculo.save()

        return JsonResponse(dict(success=True,mensaje="Se retiro"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)



# Categoria

@login_required
def categoriaList(request):
    dt_list = []
    datos = VehiculoCategoria.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,nombre=item.nombre,estado=item.estado))
    return JsonResponse(dt_list, safe=False)
@login_required
def categoriaInsert(request):
    user = request.user
    try:
        dicc = json.load(request)['obj']
        VehiculoCategoria.objects.create(**dicc)
        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def categoriaUpdate(request):
    try:
        dicc = json.load(request)['obj']
        VehiculoCategoria.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def categoriaState(request):
    try:
        dicc = json.load(request)['obj']
        obj = VehiculoCategoria.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
@login_required
def categoriaDelete(request):
    try:
        dicc = json.load(request)['obj']
        obj = VehiculoCategoria.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)