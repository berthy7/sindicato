from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from system.persona.models import Persona, PersonaReferencia
from system.linea.models import Linea,LineaVehiculo,Interno,LineaPersona,InternoVehiculo,InternoPersona
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
import json
from system.linea.models import Linea,LineaPersona
import datetime

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
            lineas = Linea.objects.filter(habilitado=True).filter(id=linea.id).all().order_by('id')
        else:
            rol = "Administrador"
            lineaUser = ""
            lineas = Linea.objects.filter(habilitado=True).all().order_by('id')
    except Exception as e:
        print(e)
    return render(request, 'conductor/index.html', {'lineas':lineas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    datos = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('-id')
    for item in datos:
        asignaciones = []
        for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
            interno = interPersona.fkinterno
            asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                                     fkinterno=interno.id, interno=interno.numero))


        dicc = model_to_dict(item)
        dicc["asignaciones"] = asignaciones
        dt_list.append(dicc)
    return JsonResponse(dt_list, safe=False)

def crear_pdf():


    logoempresa = "/resources/iconos/logo.png"

    var = "a"

    html = "" \
                    "<table style='padding: 4px; border: 0px solid grey' width='100%'>" \
                    "<tr style='font-size: 12px; border: 0px; '>" \
                    "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><img src='../servidor/common" + logoempresa + "' width='auto' height='75'></td>" \
                  "<td colspan='12' scope='colgroup'align='left'><font></font></td>" \
                  "<td colspan='5' style='border-left: 0px solid grey ' scope='colgroup'align='center'><img src='../servidor/common" + str(var) + "' width='auto' height='75'></td>" \
                "</tr>" \
                "</table>" \
                "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                "<tr color='#ffffff' >" \
                "<th colspan='22' scope='colgroup' align='left' style='background-color: #DC3131; font-size=4; color: white; margin-top: 4px'>REPORTE PERSONAL</th>" \
                "</tr>" \
                "<tr style='font-size: 12px; border: 0px; '>" \
                "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nombres y Apellidos: </strong></td>" \
                "<td colspan='12' scope='colgroup'align='left'><font>" + str(var) + "</font></td>" \
                                    "</tr>" \
                                    "<tr style='font-size: 12px; border: 0px; '>" \
                                    "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>DNI: </strong></td>" \
                                    "<td colspan='12' scope='colgroup'align='left'><font>" + str(var) + "</font></td>" \
                                               "</tr>" \
                                               "<tr style='font-size: 12px; border: 0px; '>" \
                                               "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Nacionalidad: </strong></td>" \
                                               "<td colspan='12' scope='colgroup'align='left'><font>" + var + "</font></td>" \
                                               "</tr>" \
                                               "<tr style='font-size: 12px; border: 0px; '>" \
                                               "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Fecha Nacimiento: </strong></td>" \
                                               "<td colspan='12' scope='colgroup'align='left'><font>" + var + "</font></td>" \
                                              "</tr>" \
                                              "<tr style='font-size: 12px; border: 0px; '>" \
                                              "<td colspan='5' style='border-right: 1px solid grey ' scope='colgroup'align='left'><strong>Domicilio: </strong></td>" \
                                              "<td colspan='12' scope='colgroup'align='left'><font>" + str(var) + "</font></td>" \
                                     "</tr>" \
                               "</table>" \
                               "<table style='padding: 4px; border: 1px solid grey' width='100%'>" \
                               "<tr style='font-size: 12px; border: 0px; '>" \
                               "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Tiempo de Servicio</strong></td>" \
                               "<td colspan='12' scope='colgroup'align='left'></td>" \
                               "</tr>" \
                                      "<tr style='font-size: 12px; border: 0px; '>" \
                                      "<td colspan='5' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Asistencia</strong></td>" \
                                      "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Febrero</strong></td>" \
                                      "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Marzo</strong></td>" \
                                      "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Abril</strong></td>" \
                                      "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Mayo</strong></td>" \
                                      "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Junio</strong></td>" \
                                      "<td colspan='3' style='border-right: 0px solid grey ' scope='colgroup'align='left'><strong>Julio</strong></td>" \
                                      "</tr>" \
                                      "" + var + "" \
                                                                "</table>" \
                                       "</br>"

    return html
