from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from system.persona.models import Persona, PersonaReferencia
from system.linea.models import Linea,LineaVehiculo,Interno,LineaPersona,InternoVehiculo,InternoPersona
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
import json
from system.linea.models import Linea,LineaPersona

# Create your views here.
@login_required
def index(request):
    # lineas = Linea.objects.all().order_by('id')
    # return render(request, 'conductor/index.html', {'lineas':lineas})

    user = request.user
    try:
        # persona = get_object_or_404(Persona, fkusuario=user.id)
        persona = Persona.objects.filter(fkusuario=user.id)
        if persona:
            lineaPersona = get_object_or_404(LineaPersona, fkpersona=persona[0].id)
            internos = Interno.objects.filter(fklinea=lineaPersona.fklinea.id).filter(fkpersona=None).all().order_by('id')
            lineas = Linea.objects.filter(id=lineaPersona.fklinea.id).all().order_by('id')

        else:
            internos = Interno.objects.filter(fkvehiculo=None).all().order_by('id')
            lineas = Linea.objects.all().order_by('id')

    except Exception as e:
        print(e)

    return render(request, 'conductor/index.html', { 'lineas': lineas, 'internos': internos})

@login_required
def list(request):
    dt_list = []
    datos = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('-id')
    for item in datos:

        lineas = item.lineapersona_set.filter(fkpersona=item.id).filter(estado=True)
        linId = 0
        linpersoniId = 0
        lin = "Sin linea"
        if lineas.count() > 0:
            linpersoniId = lineas[0].id
            linId = lineas[0].fklinea.id
            lin = lineas[0].fklinea.codigo

        interno = Interno.objects.get(fkpersona=item.id)
        interId = 0
        inter = "Sin Interno"
        if interno:
            interId = interno.id
            inter = interno.numero


        dt_list.append(dict(id=item.id,lineapersonaid=linpersoniId,fklinea=linId,linea=lin,fkinterno=interId,interno=inter,tipo=item.tipo,ci=item.ci,nombre=item.nombre,apellidos=item.apellidos,domicilio=item.domicilio,estado=item.estado))
    return JsonResponse(dt_list, safe=False)

@login_required
def obtain(request,id):

    persona = Persona.objects.get(id=id)

    referencias = []

    for ref in PersonaReferencia.objects.filter(fkpersona=persona.id).all().order_by('id'):
        referencias.append(model_to_dict(ref))

    dicc = model_to_dict(persona)
    response = dict(obj=dicc,referencias=referencias)

    return JsonResponse(response, safe=False)

@login_required
def insert(request):
    try:
        dicc = json.load(request)['response']
        persona = Persona.objects.create(**dicc["obj"])

        for ref in dicc["referencias"]:
            ref["fkpersona"] =  persona
            PersonaReferencia.objects.create(**ref)


        # registrar linea
        linea = Linea.objects.get(id=dicc["fklinea"])
        lineapersona = LineaPersona.objects.filter(estado=True) \
            .filter(fkpersona=persona).all()
        if len(lineapersona) >0:
            lineapersona[0].estado = False
            lineapersona[0].save()
        LineaPersona.objects.create(**dict(fkpersona=persona,fklinea=linea))

        # registrar interno
        interno = Interno.objects.get(id=dicc["fkinterno"])
        internoPersona = InternoPersona.objects.filter(estado=True) \
            .filter(fkpersona=persona).all()
        if len(internoPersona) >0:
            internoPersona[0].estado = False
            internoPersona[0].save()

        interno.fkpersona = persona
        interno.save()
        InternoPersona.objects.create(**dict(fkpersona=persona,fkinterno=interno))

        return JsonResponse(dict(success=True,mensaje="Registrado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def update(request):
    try:
        dicc = json.load(request)['obj']
        Persona.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True,mensaje="Modificado Correctamente"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def state(request):
    try:
        dicc = json.load(request)['obj']
        obj = Persona.objects.get(id=dicc["id"])
        obj.estado = dicc["estado"]
        obj.save()
        return JsonResponse(dict(success=True,mensaje="cambio de estado"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)


@login_required
def delete(request):
    try:
        dicc = json.load(request)['obj']
        obj = Persona.objects.get(id=dicc["id"])
        obj.estado = False
        obj.habilitado = False
        obj.save()
        return JsonResponse(dict(success=True,mensaje="se Eliminio"), safe=False)
    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
