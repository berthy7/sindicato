from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from system.persona.models import Persona, PersonaReferencia
from system.linea.models import Linea,LineaVehiculo,Interno,LineaPersona,InternoVehiculo,InternoPersona
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from system.incidente.models import Incidente
from system.capacitacion.models import Capacitacion
import json
from system.linea.models import Linea,LineaPersona
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

# Create your views here.
@login_required
def index(request):
    user = request.user
    try:
        persona = Persona.objects.filter(fkusuario=user.id)
        rol = persona[0].fkrol.name
        conductores = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('ci')
        if persona[0].fklinea:
            linea = get_object_or_404(Linea, id=persona[0].fklinea)
            lineaUser = linea.codigo
            lineas = Linea.objects.filter(habilitado=True).filter(id=linea.id).all().order_by('id')
            foto = persona[0].foto if persona[0].foto != None else  ""
        else:
            lineaUser = ""
            lineas = Linea.objects.filter(habilitado=True).all().order_by('id')
            foto = ""
    except Exception as e:
        print(e)
    return render(request, 'conductor/index.html', {'lineas':lineas,'conductores':conductores,
                                                   'usuario': user.first_name + " " + user.last_name,
                                                   'rol': rol,'foto': foto, 'lineaUser': lineaUser})

@login_required
def list(request):
    dt_list = []
    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    if persona[0].fklinea:
        for interPer in  InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct('fkpersona').all().select_related('fkpersona').filter(fkpersona__tipo="Conductor").filter(fkpersona__habilitado=True):
            item = interPer.fkpersona
            asignaciones = []
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by(
                    'id'):
                asignacion = model_to_dict(interPersona)
                asignacion["linea"] = interPersona.fklinea.codigo if interPersona.fklinea else '---'
                asignacion["interno"] = interPersona.fkinterno.numero if interPersona.fkinterno else '---'
                asignaciones.append(asignacion)
            dicc = model_to_dict(item)
            dicc["asignaciones"] = asignaciones
            dt_list.append(dicc)
        return JsonResponse(dt_list, safe=False)
    else:
        datos = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('-id')
        for item in datos:
            asignaciones = []
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
                asignacion = model_to_dict(interPersona)
                asignacion["linea"] = interPersona.fklinea.codigo if interPersona.fklinea else '---'
                asignacion["interno"] = interPersona.fkinterno.numero if interPersona.fkinterno else '---'
                asignaciones.append(asignacion)
            dicc = model_to_dict(item)
            dicc["asignaciones"] = asignaciones
            dt_list.append(dicc)
        return JsonResponse(dt_list, safe=False)
@login_required
def listAll(request):
    dt_list = []

    user = request.user
    persona = Persona.objects.filter(fkusuario=user.id)
    if persona[0].fklinea:
        for interPer in InternoPersona.objects.filter(fklinea=persona[0].fklinea).distinct(
                'fkpersona').all().select_related('fkpersona').filter(fkpersona__tipo="Conductor").filter(
            fkpersona__habilitado=True):
            item = interPer.fkpersona
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by(
                    'id'):
                dicc = model_to_dict(item)
                dicc["linea"] = interPersona.fklinea.codigo

                if interPersona.fkinterno:
                    dicc["interno"] = interPersona.fkinterno.numero
                else:
                    dicc["interno"] = "-"

                dt_list.append(dicc)

        return JsonResponse(dt_list, safe=False)
    else:
        datos = Persona.objects.filter(habilitado=True).filter(tipo="Conductor").all().order_by('-id')
        for item in datos:
            for interPersona in InternoPersona.objects.filter(habilitado=True).filter(fkpersona=item.id).all().order_by('id'):
                dicc = model_to_dict(item)
                dicc["linea"] = interPersona.fklinea.codigo

                if interPersona.fkinterno:
                    dicc["interno"] = interPersona.fkinterno.numero
                else:
                    dicc["interno"] = "-"

                dt_list.append(dicc)

        return JsonResponse(dt_list, safe=False)

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


        fechaHora = datetime.datetime.now() - datetime.timedelta(hours=4)
        fechaActual = fechaHora.strftime('%d/%m/%Y %H:%M')


        # p.setFont('Helvetica-Bold',12)
        p.setFont('Helvetica', 9)
        p.drawString(450,750,fechaActual)

        nombreUsuario = persona[0].nombre + ' ' + persona[0].apellidos
        p.setFont('Helvetica',9)
        p.drawString(450,765,nombreUsuario)
        # -----------------------------------------------------------

        # -----------------------------------------------------------
        p.setFont('Helvetica-Bold',10)
        p.drawString(30,710,'Nombre Conductor:')
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
        p.drawString(140,590,'Si')

        p.setFont('Helvetica-Bold', 10)
        p.drawString(400, 590, 'Fecha de Vencimiento:')
        fechavencimiento = socio.licenciaFechaVencimiento.strftime('%d/%m/%Y')
        p.setFont('Helvetica', 10)
        p.drawString(510, 590, fechavencimiento)
        # -----------------------------------------------------------

        # p.line(460,747,560,747)

        # img_file = 'static'
        # x_start = 725
        # y_start = 30
        # p.drawImage(img_file, x_start, y_start, width=120, preserveAspectRatio=True, mask='auto')

        p.setFont('Helvetica-Bold',10)
        p.drawString(30,560,'Referencias')

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
        p.drawString(30, high, 'Experiencias')

        # Table Header
        styles = getSampleStyleSheet()
        styleBH = styles['Normal']
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        c1 = Paragraph('''Linea''', styleBH)
        c2 = Paragraph('''Interno''', styleBH)
        c3 = Paragraph('''Placa''', styleBH)
        c4 = Paragraph('''Año''', styleBH)
        c5 = Paragraph('''Estado''', styleBH)

        data = [[c1, c2, c3, c4, c5]]

        # Table
        styles = getSampleStyleSheet()
        stylesN = styles['BodyText']
        stylesN.alignment = TA_CENTER
        stylesN.fontSize = 7

        high = high -20
        for ref in InternoPersona.objects.filter(fkpersona=socio.id).all().order_by('id'):
            placa = ""
            año = ""
            numero = ""
            carnet = ""
            nombre = ""
            estado = "Activo" if ref.estado else 'No Activo'

            if ref.fkinterno:
                numero = ref.fkinterno.numero
                if ref.fkinterno.fkvehiculo:
                    placa = ref.fkinterno.fkvehiculo.placa
                    año = ref.fkinterno.fkvehiculo.año
                carnet = ""
                nombre = ""
                conductor = InternoPersona.objects.filter(estado=True).filter(habilitado=True).filter(fkinterno=ref.fkinterno.id).filter(tipoPersona="Conductor").first()
                if conductor:
                    carnet = conductor.fkpersona.ci
                    nombre = conductor.fkpersona.nombre



            data.append([ref.fklinea.codigo,numero,placa,año,estado])
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
        return FileResponse(buffer, as_attachment=True, filename='Conductor.pdf')

    except Exception as e:
        return JsonResponse(dict(success=False, mensaje=e), safe=False)
