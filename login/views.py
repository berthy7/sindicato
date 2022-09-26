from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')

def logon(request):
    if request.method == 'GET':
        return render(request, '../../login/templates/index.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])

        if user is None:
            return render(request, '../../login/templates/index.html', {
                'form': AuthenticationForm,
                'error': 'username incorrecto'
            })
        else:
            login(request,user)
            return redirect('home')


def signout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'GET':
        return render(request, 'login/signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:

                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return HttpResponse("ERROR el usuario ya existe")
        return HttpResponse("password no corrrecto")

