from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from system.linea.models import Linea, LineaPersona
from system.persona.models import Persona
import json

import os.path
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.api

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

        foto = persona[0].foto if persona[0].foto != None else  ""
    except Exception as e:
        print(e)
    return render(request, 'usuario/index.html', {'lineas': lineas,'roles': roles,
                                                  'usuario': user.first_name + " " + user.last_name,
                                                'rol': rol,'foto': foto, 'lineaUser': lineaUser})
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


        dt_list.append(dict(id=item.id,fkrol=rol.id,rol=rol.name,fklinea=fklinea,linea=linea,email=item.email,usuario=item.username,
                            personaid=persona[0].id,foto=persona[0].foto,nombre=persona[0].nombre,apellidos=persona[0].apellidos))

    return JsonResponse(dt_list, safe=False)

@login_required
def listar(request):
    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    dt_list = []
    datos = User.objects.filter(~Q(username="admin")).filter(is_active=True).all().order_by('first_name')
    for item in datos:
        dt_list.append(dict(id=item.id,nombre=item.first_name +" "+item.last_name))



    dicc = dict(userid=user.id,rol=persona[0].fkrol_id,lista=dt_list)
    return JsonResponse(dicc, safe=False)

def upload_cloudinay(foto):
    resp= cloudinary.uploader.upload('static/upload/'+foto)
    return resp["secure_url"]

def handle_uploaded_file(f,name):
    with open('static/upload/'+ name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def insert(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('foto', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["persona"]['foto'] = upload_cloudinay(cname)


        del dicc["usuario"]["id"]

        user = User.objects.create_user(**dicc["usuario"])
        user.save()
        dicc["persona"]["fkusuario"] = user
        dicc["persona"]["fkrol"] = Group.objects.get(id=int(dicc["persona"]["fkrol"]))
        del dicc["persona"]["id"]
        persona = Persona.objects.create(**dicc["persona"])
        if dicc["persona"]["fklinea"] is not None:
            LineaPersona.objects.create(**dict(fkpersona=persona,fklinea=Linea.objects.get(id=int(dicc["persona"]["fklinea"]))))

        return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def update(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        files = request.FILES
        fileinfo = files.get('foto', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["persona"]['foto'] = upload_cloudinay(cname)

        usuario = User.objects.get(id=dicc["usuario"]["id"])

        usuario.username =dicc["usuario"]["username"]
        usuario.first_name=dicc["usuario"]["first_name"]
        usuario.last_name=dicc["usuario"]["last_name"]
        usuario.save()

        Persona.objects.filter(pk=dicc["persona"]["id"]).update(**dicc["persona"])

        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
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
def changefoto(request):
    try:
        dicc = json.loads(request.POST.get('obj'))

        obj = Persona.objects.get(fkusuario_id=dicc["id"])

        files = request.FILES

        fileinfo = files.get('perfil-foto', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            obj.foto = upload_cloudinay(cname)
            obj.save()

            return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
        else:
            return JsonResponse(dict(success=False, mensaje="No se envio Foto", tipo="warning"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)

@login_required
def account(request):
    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    response = dict(userid=user.id,username=user.username,foto=persona[0].foto)
    return JsonResponse(response, safe=False)