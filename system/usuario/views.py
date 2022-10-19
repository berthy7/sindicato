from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from system.linea.models import Linea, LineaPersona
from system.persona.models import Persona
import json

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        lineas = Linea.objects.all().order_by('id')
        roles = Group.objects.all().order_by('id')
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
        else:
            lineaUser = ""
    except Exception as e:
        print(e)
    return render(request, 'usuario/index.html', {'lineas': lineas,'roles': roles,
                                                  'usuario': user.first_name + " " + user.last_name,
                                                'rol': rol, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    datos = User.objects.filter(~Q(username="admin")).filter(is_active=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,usuario=item.username,nombre=item.first_name,apellidos=item.last_name))

    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        user = User.objects.create_user(**dicc["usuario"])
        user.save()
        dicc["persona"]["fkusuario"] = user
        dicc["persona"]["fkrol"] = Group.objects.get(id=int(dicc["persona"]["fkrol"]))
        persona = Persona.objects.create(**dicc["persona"])
        if dicc["persona"]["fklinea"] is not None:
            LineaPersona.objects.create(**dict(fkpersona=persona,fklinea=Linea.objects.get(id=int(dicc["fklinea"]))))


        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        usuario = User.objects.get(id=dicc["id"])

        usuario.username =dicc["usuario"]
        usuario.password=dicc["contraseña"]
        usuario.nombre=dicc["nombre"]
        usuario.apellidos=dicc["apellidos"]

        usuario.save()
        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        domicilio = User.objects.get(id=dicc["id"])
        domicilio.is_active = False
        domicilio.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
