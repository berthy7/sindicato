from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import CondominioForm
from .models import Condominio
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def condominio(request):
    # condominios = Condominio.objects.filter(nombre="nombre1",fechaRegistro__isnull=True)
    condominios = Condominio.objects.all().order_by('-id')
    return render(request, 'condominio/condominio.html', {'condominios':condominios})

@login_required
def condominio_detalle(request,id):
    if request.method == 'GET':
        condominio = get_object_or_404(Condominio,pk=id)
        form = CondominioForm(instance=condominio)
        return render(request, 'condominio/condominio_detalle.html', {'condominio':condominio, 'form':form})
    else:
        try:
            condominio = get_object_or_404(Condominio,pk=id)
            form = CondominioForm(request.POST, instance=condominio)
            form.save()

            return redirect('condominio')

        except ValueError:
            return render(request, 'condominio/create_condominio.html', {
                'condominio': condominio,
                'form': form,
                'error': 'Eror al editar'
            })

@login_required
def create_condominio(request):
    if request.method == 'GET':
        return render(request, 'condominio/create_condominio.html', {
                    'form': CondominioForm,
                })
    else:
        try:

            form = CondominioForm(request.POST)
            form.fechaRegisto= timezone.now()
            form.save()
            return redirect('condominio')
        except:
            return render(request, 'condominio/create_condominio.html', {
                'form': CondominioForm,
                'error': 'porfaor valide la data'
            })

@login_required
def condominio_eliminar(request,id):
    condominio = get_object_or_404(Condominio, pk=id)
    if request.method == 'POST':
        condominio.delete()
        return redirect('condominio')
