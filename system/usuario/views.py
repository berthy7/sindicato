from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
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
        lineas = Linea.objects.filter(habilitado=True).all().order_by('id')
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
        persona = Persona.objects.filter(fkusuario=item.id)

        rol = persona[0].fkrol

        if persona[0].fklinea:
            lin = Linea.objects.get(id=persona[0].fklinea)
            linea = lin.codigo
            fklinea = lin.id
        else:
            linea = "---"
            fklinea = 0


        dt_list.append(dict(id=item.id,fkrol=rol.id,rol=rol.name,fklinea=fklinea,linea=linea,usuario=item.username,nombre=persona[0].nombre,apellidos=persona[0].apellidos))

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
        obj = User.objects.get(id=dicc["id"])
        obj.is_active = False
        obj.username = obj.username + "DELETE" + str(obj.id)
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
@login_required
def changepassword(request):
    try:
        dicc = json.load(request)['obj']

        usuario = User.objects.get(id=dicc["id"])
        usuario.set_password(dicc["newpassword"])
        usuario.save()

        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
@login_required
def account(request):
    user = request.user
    response = dict(userid=user.id,username=user.username)

    return JsonResponse(response, safe=False)