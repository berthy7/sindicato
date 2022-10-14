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
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
        else:
            lineaUser = ""

    except Exception as e:
        print(e)

    return render(request, 'bitacora/index.html', {'usuario': user.first_name + " " + user.last_name,
                                                'rol': rol, 'lineaUser': lineaUser})


@login_required
def list(request):
    dt_list = []

    return JsonResponse(dt_list, safe=False)