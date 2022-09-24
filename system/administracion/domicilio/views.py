from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from .models import Domicilio
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

import json


@login_required
def index(request):
    return render(request, 'index.html')
    # domicilios = Domicilio.objects.all().order_by('-id')

    # return render(request, 'index.html', {'domicilios':domicilios})

@login_required
def form(request):
    if request.method == 'GET':
        return render(request, 'form.html')
    else:
        try:
            # form = CondominioForm(request.POST)
            # form.fechaRegisto= timezone.now()
            # form.save()
            return redirect('domicilio')
        except:
            return render(request, 'form.html')

def list(request):
    dt_list = []
    datos = Domicilio.objects.filter(habilitado=True).all().order_by('-id')
    for item in datos:
        dt_list.append(dict(id=item.id,codigo=item.codigo,numero=item.numero,estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def state(request):
    if request.method == 'GET':
        print("get")
        return render(request, 'condominio/create_condominio.html')
    else:
        try:
            dicc = json.load(request)['obj']
            domicilio = Domicilio.objects.get(id=dicc["id"])
            domicilio.estado = dicc["estado"]
            domicilio.save()
            return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)

        except Exception as e:
            return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    if request.method == 'GET':
        print("get")
        return render(request, 'condominio/create_condominio.html')
    else:
        try:
            dicc = json.load(request)['obj']
            domicilio = Domicilio.objects.get(id=dicc["id"])
            domicilio.estado = False
            domicilio.habilitado = False
            domicilio.save()
            return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)

        except Exception as e:
            return JsonResponse(dict(success=False, mensaje=e), safe=False)




