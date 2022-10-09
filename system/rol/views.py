from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
import json

# Create your views here.
@login_required
def index(request):
    return render(request, 'rol/index.html')

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
