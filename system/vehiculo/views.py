import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from system.vehiculoCategoria.models import VehiculoCategoria
from .models import Vehiculo
from system.linea.models import Linea,LineaVehiculo,Interno,LineaPersona,InternoVehiculo
from django.contrib.auth.models import User
from system.persona.models import Persona

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        # persona = get_object_or_404(Persona, fkusuario=user.id)
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona:
            lineaPersona = get_object_or_404(LineaPersona, fkpersona=persona[0].id)
            internos = Interno.objects.filter(fklinea=lineaPersona.fklinea.id).filter(fkvehiculo = None ).all().order_by('id')
            lineas = Linea.objects.filter(id=lineaPersona.fklinea.id).all().order_by('id')

        else:
            internos = Interno.objects.filter(fkvehiculo = None ).all().order_by('id')
            lineas = Linea.objects.all().order_by('id')

        categorias = VehiculoCategoria.objects.all().order_by('id')

    except Exception as e:
        print(e)

    return render(request, 'vehiculo/index.html', {'categorias':categorias,'lineas':lineas,'internos':internos})


@login_required
def list(request):

    dt_list = []
    datos = Vehiculo.objects.filter(habilitado=True).all().order_by('-id')

    for item in datos:

        lineas = item.lineavehiculo_set.filter(fkvehiculo= item.id).filter(estado= True)
        linId = 0
        linvehiId = 0
        lin = "Sin linea"
        if lineas.count() > 0:
            linvehiId = lineas[0].id
            linId = lineas[0].fklinea.id
            lin = lineas[0].fklinea.codigo


        interno = Interno.objects.get(fkvehiculo= item.id)
        interId = 0
        inter = "Sin Interno"
        if interno:
            interId = interno.id
            inter = interno.numero

        dt_list.append(dict(id=item.id,lineavehiculoid=linvehiId,fklinea=linId,linea=lin,fkinterno=interId,interno=inter,placa=item.placa,
                            modelo=item.modelo,tipo=item.tipo,año=item.año, categoria = item.fkcategoria.nombre, fkcategoria = item.fkcategoria.id, estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        dicc["objeto"]["fkcategoria"] = VehiculoCategoria.objects.get(id=dicc["objeto"]["fkcategoria"])

        vehiculo = Vehiculo.objects.create(**dicc["objeto"])

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

        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        obj = Vehiculo.objects.get(id=dicc["id"])
        objVehiculoCategoria = VehiculoCategoria.objects.get(id=dicc["fkcategoria"])

        obj.placa =dicc["placa"]
        obj.modelo=dicc["modelo"]
        obj.tipo=dicc["tipo"]
        obj.año=dicc["año"]
        obj.fkcategoria = objVehiculoCategoria
        obj.save()
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