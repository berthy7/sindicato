from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json

# Create your views here.
@login_required
def index(request):
    # return render(request, 'index.html')
    return render(request, '../../usuario/templates/index.html')

@login_required
def list(request):
    dt_list = []
    datos = User.objects.filter(is_active=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,usuario=item.username,nombre=item.first_name,apellidos=item.last_name))
    return JsonResponse(dt_list, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['obj']
        print(dicc)
        user = User.objects.create_user(username=dicc["usuario"],password=dicc["contraseña"] ,first_name=dicc["nombre"],last_name=dicc["apellidos"],email="")
        user.save()
        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        usuario = User.objects.get(id=dicc["id"])
        usuario.username =dicc["user"]
        usuario.password=dicc["password"]
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
