from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.conf import settings as django_settings
from .models import Persona, PersonaReferencia
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from system.linea.models import Linea,LineaPersona,Interno,InternoPersona
from system.incidente.models import Incidente
from system.capacitacion.models import Capacitacion
import json
import datetime
from django.http import FileResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,Table,TableStyle,Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

import os.path
import uuid
import io
import cloudinary
import cloudinary.uploader
import cloudinary.api

@login_required
def index(request):
    # persona = InternoPersona.objects.all()
    # for internoPer in InternoPersona.objects.all().select_related('fkinterno'):
    #     interno = internoPer.fkinterno
    #     internoPer.fklinea = interno.fklinea
    #     internoPer.save()

    user = request.user
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name

        personas = Persona.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('ci')

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

    print(lineaUser)
    return render(request, 'persona/index.html', {'lineas':lineas,'personas':personas,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    user = request.user
    admin = False
    persona = Persona.objects.filter(fkusuario=user.id)
    if persona[0].fklinea:
        admin = False
        for interPer in  InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct('fkpersona').all().select_related('fkpersona').filter(fkpersona__tipo='Socio').filter(fkpersona__habilitado=True):
            item = interPer.fkpersona
            asignaciones = []
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(
                    fkpersona=item.id).all().order_by('id'):
                interno = interPersona.fkinterno
                asignaciones.append(
                    dict(interPersonaId=interPersona.id, fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                         fkinterno=interno.id, interno=interno.numero))
            dicc = model_to_dict(item)
            dicc["asignaciones"] = asignaciones
            dt_list.append(dicc)

        obj = dict(admin=admin, lista=dt_list)
        return JsonResponse(obj, safe=False)
    else:
        datos = Persona.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('-id')
        admin = True
        for item in datos:
            asignaciones = []
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
                interno = interPersona.fkinterno
                asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
                                         fkinterno=interno.id, interno=interno.numero))
            dicc = model_to_dict(item)
            dicc["asignaciones"] = asignaciones
            dt_list.append(dicc)

        obj = dict(admin=admin, lista=dt_list)
        return JsonResponse(obj, safe=False)

@login_required
def listAll(request):
    dt_list = []

    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    if persona[0].fklinea:
        for interPer in InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct(
                'fkpersona').all().select_related('fkpersona').filter(fkpersona__tipo="Socio").filter(
            fkpersona__habilitado=True):
            item = interPer.fkpersona
            for interPersona in InternoPersona.objects.filter(fklinea=persona[0].fklinea).filter(habilitado=True).filter(fkpersona=item.id).all().order_by(
                    'id'):

                dicc = model_to_dict(item)
                dicc["linea"] = interPersona.fklinea.codigo
                dicc["interno"] = interPersona.fkinterno.numero
                dt_list.append(dicc)

        return JsonResponse(dt_list, safe=False)
    else:
        datos = Persona.objects.filter(habilitado=True).filter(tipo="Socio").all().order_by('-id')
        for item in datos:
            print(item.id)
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
                dicc = model_to_dict(item)
                dicc["linea"] = interPersona.fklinea.codigo
                dicc["interno"] = interPersona.fkinterno.numero
                dt_list.append(dicc)

        return JsonResponse(dt_list, safe=False)
@login_required
def obtain(request,id):
    persona = Persona.objects.get(id=id)
    if persona.fechaNacimiento:
        persona.fechaNacimiento = persona.fechaNacimiento.strftime('%d/%m/%Y')
    if persona.licenciaFechaVencimiento:
        persona.licenciaFechaVencimiento = persona.licenciaFechaVencimiento.strftime('%d/%m/%Y')
    referencias = []
    for ref in PersonaReferencia.objects.filter(habilitado=True).filter(fkpersona=persona.id).all().order_by('id'):
        referencias.append(model_to_dict(ref))
    asignaciones = []
    for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=persona.id).all().order_by('id'):

        # interno = interPersona.fkinterno
        #
        # asignaciones.append(dict(interPersonaId=interPersona.id,fklinea=interno.fklinea_id, linea=interno.fklinea.codigo,
        #                          fkinterno=interno.id, interno=interno.numero))
        asignacion = model_to_dict(interPersona)

        asignacion["interPersonaId"] = interPersona.id
        asignacion["linea"] = interPersona.fklinea.codigo if interPersona.fklinea else '---'
        asignacion["interno"] = interPersona.fkinterno.numero if interPersona.fkinterno else '---'
        asignaciones.append(asignacion)

    dicc = model_to_dict(persona)
    response = dict(obj=dicc,referencias=referencias,asignaciones=asignaciones)

    return JsonResponse(response, safe=False)


def upload_cloudinay(foto):
    resp= cloudinary.uploader.upload('static/upload/'+foto)
    return resp["secure_url"]

def handle_uploaded_file(f,name):
    with open('static/upload/'+ name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def insertfile(request):
    try:
        dicc = json.loads(request.POST.get('obj'))
        obj = Persona.objects.get(id=dicc['id'])
        files = request.FILES

        fileinfo = files.get('foto', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            obj.foto = upload_cloudinay(cname)

        fileinfo = files.get('file-ci', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            obj.fotoCi = upload_cloudinay(cname)

        fileinfo = files.get('file-licencia', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            obj.fotoLicencia = upload_cloudinay(cname)

        obj.save()
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)


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
            handle_uploaded_file(fileinfo,cname)
            dicc["obj"]['foto'] = upload_cloudinay(cname)

        fileinfo = files.get('file-ci', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo,cname)
            dicc["obj"]['fotoCi'] = upload_cloudinay(cname)


        fileinfo = files.get('file-licencia', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc["obj"]['fotoLicencia'] = upload_cloudinay(cname)

        # dicc = json.load(request)['obj']
        persona = Persona.objects.filter(ci=dicc["obj"]['ci']).filter(habilitado=True).all()

        if len(persona) == 0:

            if dicc["obj"]['fechaNacimiento'] != "":
                dicc["obj"]['fechaNacimiento'] = datetime.datetime.strptime(dicc["obj"]['fechaNacimiento'],'%d/%m/%Y')
            else:
                dicc["obj"]['fechaNacimiento'] = None

            if dicc["obj"]['licenciaFechaVencimiento'] != "":
                dicc["obj"]['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc["obj"]['licenciaFechaVencimiento'],'%d/%m/%Y')
            else:
                dicc["obj"]['licenciaFechaVencimiento'] = None
            try:
                if dicc["obj"]['fechaInscripcion'] != "":
                    dicc["obj"]['fechaInscripcion'] = datetime.datetime.strptime(
                        dicc["obj"]['fechaInscripcion'], '%d/%m/%Y')
                else:
                    dicc["obj"]['fechaInscripcion'] = None

            except Exception as e:
                print("error en cath: ", e.args[0])
                dicc["obj"]['fechaInscripcion'] = None

            del dicc["obj"]['id']

            persona = Persona.objects.create(**dicc["obj"])

            for ref in dicc["referencias"]:
                del ref['id']
                ref["fkpersona"] =  persona
                PersonaReferencia.objects.create(**ref)

            for asig in dicc["lineas"]:
                asig["fklinea"] = Linea.objects.get(id=asig["fklinea"])
                asig["fkinterno"] =  Interno.objects.get(id=asig["fkinterno"])
                asig["fkpersona"] = persona
                asig["tipoPersona"] = dicc["obj"]['tipo']
                del asig['interPersonaId']
                del asig['linea']
                del asig['interno']
                InternoPersona.objects.create(**asig)

            return JsonResponse(dict(success=True, mensaje="Registrado Correctamente", tipo="success"), safe=False)
        else:
            return JsonResponse(dict(success=False, mensaje="El Ci ya esta registrado en el sistema", tipo="warning"), safe=False)

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
            dicc['foto'] = upload_cloudinay(cname)


        fileinfo = files.get('file-ci', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc['fotoCi'] = upload_cloudinay(cname)

        fileinfo = files.get('file-licencia', None)
        if fileinfo:
            fname = fileinfo.name
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            handle_uploaded_file(fileinfo, cname)
            dicc['fotoLicencia'] = upload_cloudinay(cname)


        if dicc['fechaNacimiento'] != "":
            dicc['fechaNacimiento'] = datetime.datetime.strptime(dicc['fechaNacimiento'],'%d/%m/%Y')
        else:
            dicc['fechaNacimiento'] = None
        if dicc['licenciaFechaVencimiento'] != "":
            dicc['licenciaFechaVencimiento'] = datetime.datetime.strptime(dicc['licenciaFechaVencimiento'], '%d/%m/%Y')
        else:
            dicc['licenciaFechaVencimiento'] = None

        try:
            if dicc['fechaInscripcion'] != "":
                dicc['fechaInscripcion'] = datetime.datetime.strptime(
                    dicc['fechaInscripcion'], '%d/%m/%Y')
            else:
                dicc['fechaInscripcion'] = None

        except Exception as e:
            print("error en cath: ", e.args[0])
            dicc["obj"]['fechaInscripcion'] = None

        Persona.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Modificado Correctamente", tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error", tipo="error"), safe=False)
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

@login_required
def reporte(request,id):
    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    try:

        socio = Persona.objects.get(id=id)

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()
        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer, pagesize=letter)

        # Header
        p.setLineWidth(.3)
        p.setFont('Helvetica-Bold',12)
        p.drawString(30,750,'SINDICATO DE TRANSPORTISTAS SANTA CRUZ')

        # p.setFont('Helvetica-Bold',12)
        p.setFont('Helvetica', 9)
        p.drawString(450,750,datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))

        nombreUsuario = persona[0].nombre + ' ' + persona[0].apellidos
        p.setFont('Helvetica',9)
        p.drawString(450,765,nombreUsuario)

        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,730,'Fecha de inscripción:')
        fecha = socio.fechaInscripcion.strftime('%d/%m/%Y') if socio.fechaInscripcion else '----'
        p.setFont('Helvetica',10)
        p.drawString(140,730,fecha)
        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,710,'Nombre Socio:')
        p.setFont('Helvetica',10)
        p.drawString(140,710,socio.nombre + ' '+ socio.apellidos)
        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,690,'Carnet:')
        p.setFont('Helvetica',10)
        p.drawString(140,690,socio.ci + " " + socio.lugarNacimiento)
        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,670,'Telefono:')
        p.setFont('Helvetica',10)
        p.drawString(140,670,socio.telefono)

        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,650,'Domicilio:')
        p.setFont('Helvetica',10)
        p.drawString(140,650,socio.domicilio)

        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,630,'Fecha de Nacimiento:')
        fecha =  socio.fechaNacimiento.strftime('%d/%m/%Y') if socio.fechaNacimiento else '----'
        p.setFont('Helvetica',10)
        p.drawString(140,630,fecha)

        p.setFont('Helvetica-Bold',10)
        p.drawString(400,630,'Licencia:')
        p.setFont('Helvetica',10)
        p.drawString(510,630,socio.licenciaNro)

        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,610,'Genero:')
        p.setFont('Helvetica',10)
        p.drawString(140,610,socio.genero)

        p.setFont('Helvetica-Bold',10)
        p.drawString(400,610,'Categoria:')
        p.setFont('Helvetica',10)
        p.drawString(510,610,socio.licenciaCategoria)

        # -----------------------------------------------------------

        p.setFont('Helvetica-Bold',10)
        p.drawString(30,590,'Conduce:')
        p.setFont('Helvetica',10)
        p.drawString(140,590,socio.socioConductor)

        p.setFont('Helvetica-Bold', 10)
        p.drawString(400, 590, 'Fecha de Vencimiento:')
        fechavencimiento = socio.licenciaFechaVencimiento.strftime('%d/%m/%Y') if socio.licenciaFechaVencimiento else '----'
        p.setFont('Helvetica', 10)
        p.drawString(510, 590, fechavencimiento)
        # -----------------------------------------------------------

        # p.line(460,747,560,747)

        # img_file = 'static'
        # x_start = 725
        # y_start = 30
        # p.drawImage(img_file, x_start, y_start, width=120, preserveAspectRatio=True, mask='auto')

        p.setFont('Helvetica-Bold',10)
        p.drawString(30,560,'Beneficiarios')

        # Table Header
        styles = getSampleStyleSheet()
        styleBH = styles['Normal']
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        c1 = Paragraph('''Parentesco''',styleBH)
        c2 = Paragraph('''Carnet''',styleBH)
        c3 = Paragraph('''Nombre''', styleBH)
        c4 = Paragraph('''Apellidos''', styleBH)
        c5 = Paragraph('''Telefono''', styleBH)

        data = [[c1,c2,c3,c4,c5]]

        # Table
        styles = getSampleStyleSheet()
        stylesN = styles['BodyText']
        stylesN.alignment = TA_CENTER
        stylesN.fontSize = 7

        high = 540

        for ref in PersonaReferencia.objects.filter(habilitado=True).filter(fkpersona=socio.id).all().order_by('id'):
            data.append([ref.categoria,ref.ci,ref.nombre,ref.apellidos,ref.telefono])
            high = high - 18

        # Table size
        width, height = letter
        table = Table(data,colWidths=None)
        table.setStyle(TableStyle([
            ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
            ('BOX',(0,0),(-1,-1),0.25,colors.black),]))

        table.wrapOn(p,width-40,height)
        table.drawOn(p,20,high)

        # -----------------------------------------------------------
        high = high - 20
        p.setFont('Helvetica-Bold', 10)
        p.drawString(30, high, 'Lineas')

        # Table Header
        styles = getSampleStyleSheet()
        styleBH = styles['Normal']
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        c1 = Paragraph('''Linea''', styleBH)
        c2 = Paragraph('''Interno''', styleBH)
        c3 = Paragraph('''Placa''', styleBH)
        c4 = Paragraph('''Año''', styleBH)
        c5 = Paragraph('''Carnet''', styleBH)
        c6 = Paragraph('''Nombre''', styleBH)

        data = [[c1, c2, c3, c4, c5, c6]]

        # Table
        styles = getSampleStyleSheet()
        stylesN = styles['BodyText']
        stylesN.alignment = TA_CENTER
        stylesN.fontSize = 7

        high = high -20
        for ref in InternoPersona.objects.filter(estado=True).filter(habilitado=True).filter(fkpersona=socio.id).all().order_by('id'):
            placa = ""
            año = ""
            if ref.fkinterno.fkvehiculo:
                placa = ref.fkinterno.fkvehiculo.placa
                año = ref.fkinterno.fkvehiculo.año
            carnet = ""
            nombre = ""
            conductor = InternoPersona.objects.filter(estado=True).filter(habilitado=True).filter(fkinterno=ref.fkinterno.id).filter(tipoPersona="Conductor").first()
            if conductor:
                carnet = conductor.fkpersona.ci
                nombre = conductor.fkpersona.nombre

            data.append([ref.fkinterno.fklinea.codigo,ref.fkinterno.numero,placa,año,
                         carnet,nombre])
            high = high - 18

        # Table size
        width, height = letter
        table = Table(data, colWidths=None)
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

        table.wrapOn(p, width - 40, height)
        table.drawOn(p, 20, high)

        # -----------------------------------------------------------
        high = high - 20
        p.setFont('Helvetica-Bold', 10)
        p.drawString(30, high, 'Incidentes')

        # Table Header
        styles = getSampleStyleSheet()
        styleBH = styles['Normal']
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        c1 = Paragraph('''Linea''', styleBH)
        c2 = Paragraph('''Fecha''', styleBH)
        c3 = Paragraph('''Incidente''', styleBH)
        c4 = Paragraph('''Descripción''', styleBH)
        c5 = Paragraph('''Estado''', styleBH)

        data = [[c1, c2, c3, c4, c5]]

        # Table
        styles = getSampleStyleSheet()
        stylesN = styles['BodyText']
        stylesN.alignment = TA_CENTER
        stylesN.fontSize = 7

        high = high - 20

        for obj in Incidente.objects.filter(habilitado=True).filter(fkpersona=socio.id).all().order_by('fecha'):

            data.append([obj.fklinea.codigo, obj.fecha.strftime('%d/%m/%Y'), obj.fktipo.nombre, obj.descripcion, obj.estados])
            high = high - 18

        # Table size
        width, height = letter
        table = Table(data, colWidths=None)
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

        table.wrapOn(p, width - 40, height)
        table.drawOn(p, 20, high)

        # -----------------------------------------------------------
        high = high - 20
        p.setFont('Helvetica-Bold', 10)
        p.drawString(30, high, 'Capacitaciones')

        # Table Header
        styles = getSampleStyleSheet()
        styleBH = styles['Normal']
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        c1 = Paragraph('''Fecha''', styleBH)
        c2 = Paragraph('''Curso''', styleBH)
        c3 = Paragraph('''Descripción''', styleBH)
        c4 = Paragraph('''Dictado por''', styleBH)

        data = [[c1, c2, c3, c4]]

        # Table
        styles = getSampleStyleSheet()
        stylesN = styles['BodyText']
        stylesN.alignment = TA_CENTER
        stylesN.fontSize = 7

        high = high - 20

        for obj in Capacitacion.objects.filter(habilitado=True).filter(fkpersona=socio.id).all().order_by('fecha'):
            data.append(
                [obj.fecha.strftime('%d/%m/%Y'), obj.fkcurso.nombre, obj.descripcion,obj.dictado ])
            high = high - 18

        # Table size
        width, height = letter
        table = Table(data, colWidths=None)
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

        table.wrapOn(p, width - 40, height)
        table.drawOn(p, 20, high)

        # -----------------------------------------------------------

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Socio.pdf')

    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)

@login_required
def listarPersonaXTipo(request,id):
    dt_list = []
    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    if persona[0].fklinea:
        for interPer in InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct(
                'fkpersona').all().select_related('fkpersona').filter(fkpersona__tipo=id).filter(fkpersona__habilitado=True):
            item = interPer.fkpersona
            dt_list.append(dict(id=item.id, nombre=item.nombre + " " + item.apellidos))
        return JsonResponse(dt_list, safe=False)

    else:
        datos = Persona.objects.filter(habilitado=True).filter(tipo=id).all().order_by('nombre')
        for item in datos:
            dt_list.append(dict(id=item.id, nombre=item.nombre + " " + item.apellidos))

        return JsonResponse(dt_list, safe=False)


@login_required
def agregarInternos(request):
    try:
        dicc = json.load(request)['obj']

        del dicc['interPersonaId']
        del dicc['linea']
        del dicc['interno']

        dicc['fklinea'] = Linea.objects.get(id=dicc["fklinea"])

        if dicc["fkinterno"] != '':
            dicc['fkinterno'] = Interno.objects.get(id=dicc["fkinterno"])
        else:
            dicc['fkinterno'] = None

        dicc['fkpersona'] = Persona.objects.get(id=dicc["fkpersona"])

        dicc['tipoPersona'] = dicc['fkpersona'].tipo
        InternoPersona.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Agregado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def eliminarInternos(request,id):
    try:
        interno = InternoPersona.objects.get(id=id)
        interno.estado = False
        interno.habilitado = False
        interno.fechaRetiro = datetime.datetime.now()
        interno.save()
        return JsonResponse(dict(success=True, mensaje="Eliminado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def eliminarReferencia(request,id):
    try:
        referencia = PersonaReferencia.objects.get(id=id)
        referencia.estado = False
        referencia.habilitado = False
        referencia.save()
        return JsonResponse(dict(success=True, mensaje="Eliminado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def agregarReferencia(request):
    try:
        dicc = json.load(request)['obj']
        dicc['fkpersona'] = Persona.objects.get(id=dicc["fkpersona"])
        del dicc['id']
        PersonaReferencia.objects.create(**dicc)

        return JsonResponse(dict(success=True, mensaje="Agregado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
@login_required
def modificarReferencia(request):
    try:
        dicc = json.load(request)['obj']
        dicc['fkpersona'] = Persona.objects.get(id=dicc["fkpersona"])
        PersonaReferencia.objects.filter(pk=dicc["id"]).update(**dicc)
        return JsonResponse(dict(success=True, mensaje="Actualizado Correctamente",tipo="success"), safe=False)
    except Exception as e:
        print("error: ", e.args[0])
        return JsonResponse(dict(success=False, mensaje="Ocurrió un error",tipo="error"), safe=False)
