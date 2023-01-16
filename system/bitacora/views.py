from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from system.persona.models import Persona
from system.linea.models import Linea

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        # persona = get_object_or_404(Persona, fkusuario=user.id)
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name

        usuarios = User.objects.filter(is_active=True).filter(is_superuser=False).order_by('first_name')

        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
        else:
            lineaUser = ""

        foto = persona[0].foto if persona[0].foto != None else  ""

    except Exception as e:
        print(e)

    return render(request, 'bitacora/index.html', {'usuario': user.first_name + " " + user.last_name,
                                             'usuarios': usuarios,'rol': rol,'foto': foto, 'lineaUser': lineaUser})


@login_required
def list(request):
    dt_list = []
    dicc = json.load(request)['obj']
    try:

        if(dicc["opcion"] == "Linea"):
            if (dicc["accion"] == "Registro"):
                dt_list = listar_registro_lineas(dicc["usuario"])
            else:
                dt_list = listar_elimino_lineas(dicc["usuario"])

        elif(dicc["opcion"] == "Socios"):
            dt_list = listar_socios(dicc["accion"], dicc["usuario"])
        elif(dicc["opcion"] == "TransferenciaSocios"):
            dt_list = listar_sociosTrans(dicc["accion"], dicc["usuario"])



        return JsonResponse(dict(response=dt_list,success=True, mensaje="listado Correctamente", tipo="success"), safe=False)

    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)


def listar_registro_lineas(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Linea.objects.filter(fkusuario_id=int(usuario)).all().order_by('id')
    else:
        datos = Linea.objects.all().order_by('id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i,fecha=item.fechar.strftime('%d/%m/%Y'),
                            nombre=item.fkusuario.first_name + " " +item.fkusuario.last_name,
                            id=item.id,registro=item.codigo))
    return dt_list


def listar_elimino_lineas(usuario):
    dt_list = []
    i = 0
    if usuario != '':
        datos = Linea.objects.filter(habilitado=False).filter(fkusuario_id=int(usuario)).all().order_by('id')
    else:
        datos = Linea.objects.filter(habilitado=False).all().order_by('id')
    for item in datos:
        i = i+1
        dt_list.append(dict(nro=i,fecha= item.fechaEliminado.strftime('%d/%m/%Y'),
                            nombre=item.fkusuarioEliminado.first_name + " " +item.fkusuarioEliminado.last_name,
                            id=item.id,registro=item.codigo))
    return dt_list





def listar_socios(accion,usuario):

    return []


def listar_sociosTrans(accion,usuario):

    return []