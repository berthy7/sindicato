from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from system.linea.models import Linea
from system.persona.models import Persona
from system.vehiculo.models import Vehiculo
from system.linea.models import Interno
import json



def funcion():
    vehiculos = Vehiculo.objects.filter(estado = True).filter(habilitado=True)
    print("inicio funcion")
    for vehiculo in vehiculos:
        interno = Interno.objects.get(id=vehiculo.fkinterno)
        interno.fkvehiculo =vehiculo
        interno.save()
    print ("fin funcion")

# Create your views here.
@login_required
def index(request):
    # funcion()

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
    return render(request, 'rol/index.html', {'usuario': user.first_name + " " + user.last_name,
                                                'rol': rol,'foto': foto, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    datos = Group.objects.all().order_by('id')
    for item in datos:
        dt_list.append(dict(id=item.id,name=item.name))
    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        Group.objects.create(name=dicc["nombre"])
        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        obj = Group.objects.get(id=dicc["id"])
        obj.nombre =dicc["nombre"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
