from django.shortcuts import render, get_object_or_404, render_to_response, redirect # is used to looks for the object that is related the call
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.template import Context
import datetime
from math import ceil
from django.core.mail import send_mail
from controlescolar.models import Estudiante, Curso, Materia, Catalogo, Documentacion
from promotoria.models import Aspirantes
from contabilidad.models import EgresoGenerales, EgresoNomina, Tarjeton, PagosAlumno,CorteCaja
from siad.models import Empleado, Documento, Calendario
from .forms import rango_fechas_form,fecha_form, preguntas_form, form_acceso_alumno, form_captura_cal, form_boleta_alumno,form_plantel_empresa_horario,form_genera_extraordinario,form_busca_alumno_nombre,empresaFecha_form,fechaPlantel_form, form_empresa, form_plantel, form_corte_caja,form_no_alumno,rango_fechas_plantel_form,rango_fechas_calendario_form,form_alumno_materia
from .tables import AspiranteTable, EstudianteTable, PagosProximosTable, PagosProximosNominaTable,PagospendientesTable
import csv
from django_tables2 import RequestConfig
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from .modules import rutinas as rut
from .modules import generadorTEX as tex
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import os
from io import BytesIO
#from reportlab.pdfgen import canvas
from django.http import HttpResponse

def descarga(request,archivo):
	print("### Abriendo el archivo",archivo)
	ff = open(archivo,"rb")
	response = HttpResponse(ff.read(), content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="%s"'%(archivo.split("_")[-1])
	ff.close()
	print("### Se ha creado y entregado el archivo")
	return response

def genera_archivo_PDF(request,alumno,materia,privilegios = False):
	try:
		qs_alumno = Estudiante.objects.get(id=alumno)
	except:
		context = {
			'titulo': "Registro inexistente",
			'mensaje': "Ese alumno no existe en la base de datos",
		}
		return render(request, 'msg_registro_inexistente.html',context)
	try:
		qs_materia = Materia.objects.get(id=materia)
	except:
		context = {
			'titulo': "Registro inexistente",
			'mensaje': "Esa materia no existe en la base de datos",
		}
		return render(request, 'msg_registro_inexistente.html',context)
	hoy = timezone.localtime(timezone.now()).date()
	if hoy<qs_materia.fecha_inicio or hoy>qs_materia.fecha_termino:
		print("### Fuera de fechas")
		context = {
		'titulo': "Fuera de fechas",
		'mensaje': "Este material ya no esta vigente",
		}
		if privilegios ==False:
		    return render(request, 'msg_registro_inexistente.html',context)
	nombre_materia = str(qs_materia.nombre).replace(" ","")
	materia = "%d_%d_%s"%(qs_materia.id,qs_alumno.id,nombre_materia)

	archivo_pdf = "pdfs/" + str(materia) + ".pdf"
	if os.path.exists(archivo_pdf):
		print("### El archivo ya existe, solo se descarga")
		if privilegios == False:
		    return descarga(request,archivo_pdf)
	print("### El archivo no existe o lo esta generando el administrador, se genera un archivo nuevo")
	nombre = str(materia)  + ".tex"
	a = qs_materia.banco.archivo
	try:
		print("### Abriendo el archivo del banco")
		a.open("r")
		lineas = a.readlines()
		a.close()

	except:
		print("### No se pudo abrir el banco")
		context = {
		'titulo': "SIN BANCO DE REACTIVOS",
		'mensaje': "Esta materia no tiene un banco de reactivos dado de alta",
		}
		return render(request, 'msg_registro_inexistente.html',context)
	a.open("r")
	lineas = a.readlines()
	a.close()
	for i in range(len(lineas)):
		#linea = lineas[i].replace("\\\\","\\")
		#print("Directo del archivo",lineas[i],type(lineas[i]))
		linea = str(lineas[i])
		if linea[0]=="b":
			lineas[i] = linea[1:]
		else:
			lineas[i] = linea
		#lineas[i] = lineas[i].replace("|","")
		#print("Directo del archivo",lineas[i])
	contenido = {
	"alumno":"%d %s %s %s"%(qs_alumno.id,qs_alumno.Aspirante.nombre,qs_alumno.Aspirante.apellido_paterno,qs_alumno.Aspirante.apellido_materno),
	"materia": "%s"%(nombre_materia),
	"claveMateria": qs_materia.id,
	"n_preguntas": qs_materia.banco.numero_de_reactivos,
	"folio": qs_alumno.numero_de_control,
	"en_orden": qs_materia.banco.preguntas_en_el_mismo_orden,
	"lineas": lineas,
	"nombreBanco":qs_materia.banco.nombre_del_examen
	}
	tex.crea_archivo(nombre,contenido)
	if os.path.exists(archivo_pdf):
		print("### El archivo se descarga inmediatamente despues de haber sido creado")
		return descarga(request,archivo_pdf)

	context={"mensaje":"No se pudo generar el material"}
	return render(request, "tabla_general.html", context)

def genera_pdf(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

	buffer = BytesIO()

	# Create the PDF object, using the BytesIO object as its "file."
	p = canvas.Canvas(buffer)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(100, 100, "Hello world.")

	# Close the PDF object cleanly.
	p.showPage()
	p.save()

	# Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
def generate_csvFile(request,datos = None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    fileName = datos['claveAlumno']+datos['claveExamen']+'.csv'
    response['Content-Disposition'] = 'attachment; filename=%s'%fileName

    writer = csv.writer(response)
    writer.writerow([datos['nombre'], datos['claveAlumno'], datos['numeroPreguntas'], datos['claveExamen'], datos['versionExamen']])
    writer.writerow(datos['listaRespuestas'])

    return response

# Create your views here.
def cobros_vencidos(request,dias):

	#cursos = Curso.objects.filter(estudiante__documentacion__documentacion_completa=False)
	queryset = Tarjeton.objects.filter(monto_cubierto = False,alumno__activo=True)
	queryset = queryset.filter(pagos_atrasados__gt = 0 )
	filas=[]
	cnt = 0
	encabezados = ["Alumno","Pagos atrasados","Monto","Horario","Fecha del pago"]
	montoTotal = 0
	for tar in queryset:
		#diasAtraso = datetime.date.today()-tar.proxima_fecha_de_pago
		atrasos = tar.pagos_atrasados
		monto = tar.deuda_actual
		fila = [tar.alumno,atrasos,monto,tar.alumno.curso.horario,tar.proxima_fecha_de_pago]
		filas.append(fila)
		montoTotal += monto
	context = {"filas":filas,
			 	'mensaje': "Cobros vencidos",
				'submensaje': "La suma total de pagos vencidos es $" + str(montoTotal),
				"encabezados":encabezados,
				}
	return render(request,"reporta_resultados.html", context)
	pagosAlumnos = PagosAlumno.objects.filter(fecha_pago=datetime.date.today())
	total = 0
	filas = []
	cnt=0
	for pago in pagosAlumnos:
		total += pago.monto
		fila = [pago.fecha_pago,pago.alumno,pago.monto,pago.forma_de_pago,pago.folio]
		cnt += 1
		filas.append(fila)
	context = {
			'mensaje': "Se registraron %d movimientos el dia de hoy"%cnt,
			'submensaje': "La suma de ingresos registrados es de $" + str(total),
			'encabezados': ['Fecha','Pago','Monto','Forma de pago','Folio'],
			'filas': filas,
			}
	return render(request, "reporta_resultados.html", context)
#def index(request):
def respuestas(request,materia):
	idAlumno = request.session["id_alumno"]
	alumno_qs = Estudiante.objects.get(id=idAlumno)
	folio = str(alumno_qs.numero_de_control)
	nombre = str(alumno_qs)
	try:
		materia_qs = Materia.objects.get(id=materia)
	except:

		context = {
			'titulo': "MATERIA INEXISTENTE",
			'mensaje': "Esa materia no esta registrada en la base de datos",
		}

		return render(request, 'msg_registro_inexistente.html',context)
	claveExamen = "1111"
	if materia_qs.banco.preguntas_en_el_mismo_orden==True:
		claveExamen = "0111"
	numeroPreguntas = materia_qs.banco.numero_de_reactivos
	materiaEncontrada= 0
	curso = Curso.objects.get(estudiante = idAlumno)
	boleta=curso.boleta
	for linea in boleta.split('\n'):
		if len(linea)!=0 : # si la linea contiene informacion
			print('La linea contiene',linea)
			mat = linea.split()[0]
			print('La materia en la boleta es',mat,' la materia en la consulta es ',materia)
			if int(mat)==int(materia):
				respuestasDesencriptadas = rut.desencripta(linea.split()[-1])
				materiaEncontrada = 1
				break
	listaRespuestas = respuestasDesencriptadas
	calif,incorr,correc,noContestadas= rut.evaluacionDigital(nombreAlumno=nombre,claveAlumno= folio,claveExamen = claveExamen,versionExamen=2017,nPreguntas=numeroPreguntas,materia="Aqui va una materia",listaPreguntas=listaRespuestas)
	#return generate_csvFile(request,datos)
	queryset2 = Materia.objects.filter(id=materia)
	materiaNombre = "%d: %s"%(queryset2[0].id,queryset2[0].nombre)
	lista = [
	["Nombre del alumno: ",nombre],
	#["Folio del alumno: ",folio],
	["Materia: ",materiaNombre],
	["Calificacion:",calif],
	["Incorrectas contestadas por el alumno (%d):"%(len(incorr)),incorr],
	["Correctas contestadas por el alumno (%d):"%(len(correc)),correc],
	#["Sin contestar (%d)"%(len(noContestadas)),noContestadas]
	]
	context={
		'mensaje': "El resultado de la evaluacion es:",
		'lista':lista,
	}
	# ahora que se ha evaluado el examen es necesario asentar la calificacion en la boleta
	# 1.- Hacer la consulta para saber que curso le corresponde al alumno
	# 2.- En el curso correspondiente se debe de verificar dos cosas:
	#     2.1.- Verificar si la materia ya esta dada de alta en la boleta.
	#     2.2.- Verificar que el alumno no tenga mas de tres intentos.
	# 3.- Asentar la calificacion en la boleta
	################################################
	#curso = Curso.objects.get(estudiante = idAlumno)
	#print('EL CONTENIDO DEL CURSO ES:')
	#curso = curso
	#print(curso,curso.materias.all())
	#boleta = str(curso.boleta)

	#print('EL CONTENIDO DE LA BOLETA ESSSS:')
	#print(boleta.split('\n'))
	#print(boleta.split('\r'))
	#boletaNueva = rut.agrega_calificacion(boleta.split('\n'),materia,calif,cadenaRespuestas)
	#print('Boleta antigua',boleta)
	#print('SEPARADOR ENTRE BOLETAS')
	#print('Boleta Nueva',boletaNueva)
	#if boletaNueva == -1:
	#	context = {
	#		'titulo': "NO MAS INTENTOS",
	#		'mensaje': "Solo se permiten tres evaluaciones por materia",
	#	}

	#	return render(request, 'msg_registro_inexistente.html',context)

	#Curso.objects.filter(pk=curso.pk).update(boleta=boletaNueva)
	#return HttpResponseRedirect("/alumnos")
	return render(request,'impresion_lista_2d.html',context)
def evaluacion_digital(request,alumno,materia):
	""" This function allows to record the grade of the alumn in the corresponding alumno's "boleta"
	"""
	if request.method == 'POST':
		form = preguntas_form(request.POST)
		if form.is_valid():
			queryset = Estudiante.objects.filter(id = alumno)
			if len(queryset)==0:
				print('NO EXISTE ESE ALUMNO')
				return render(request, 'msg_registro_inexistente.html')
			nombre = str(queryset[0])
			claveAlumno = str(queryset[0].numero_de_control)

			#nombre = form.cleaned_data['nombre']
			#claveAlumno = form.cleaned_data['clave_de_alumno']
			#numeroPreguntas = form.cleaned_data['numero_de_preguntas']
			qs_materia = Materia.objects.get(id=materia)
			id_banco = qs_materia.banco.id
			numeroPreguntas = Catalogo.objects.get(id=id_banco).numero_de_reactivos
			print("La materia es ",qs_materia,"banco",id_banco,"n preguntas",numeroPreguntas)
			#claveExamen = form.cleaned_data['clave_del_examen']
			claveExamen = "1111"
			#versionExamen = form.cleaned_data['version_examen']
			listaRespuestas = []
			cadenaRespuestas = ""
			for i in range(1,int(numeroPreguntas)+1):
				cadenaPregunta = 'pregunta_%d'%i
				valor = form.cleaned_data[cadenaPregunta]
				if valor == '':
					calor = -1
				else:
					valor=int(valor)
				listaRespuestas.append(valor)
				cadenaRespuestas += str(valor)
			print("respuestas enviadas son:" ,cadenaRespuestas)
			encriptado = rut.encripta(cadenaRespuestas)
			print("respuestas encriptadas son:" ,encriptado)
			print('Las respuestas desencriptadas son:',rut.desencripta(encriptado))
			#print(nombre,claveAlumno,numeroPreguntas,claveExamen)
			datos = {'nombre':nombre,
			'claveAlumno':claveAlumno,
			'numeroPreguntas':numeroPreguntas,
			'claveExamen':claveExamen,
			'listaRespuestas':listaRespuestas,
			}
			calif,incorr,correc,noContestadas= rut.evaluacionDigital(nombreAlumno=nombre,claveAlumno= claveAlumno,claveExamen = claveExamen,versionExamen=2017,nPreguntas=numeroPreguntas,materia="Aqui va una materia",listaPreguntas=listaRespuestas)
			#return generate_csvFile(request,datos)
			queryset2 = Materia.objects.filter(id=materia)
			materiaNombre = queryset2[0].nombre
			lista = [
			["Nombre del alumno: ",nombre],
			["Folio del alumno: ",claveAlumno],
			["Materia: ",materiaNombre],
			["Calificacion",calif],
			["Incorrectas (%d)"%(len(incorr)),incorr],
			["Correctas (%d)"%(len(correc)),correc],
			["Sin contestar (%d)"%(len(noContestadas)),noContestadas]
			]
			context={
				'mensaje': "El resultado de la evaluacion es:",
				'lista':lista,
			}
			# ahora que se ha evaluado el examen es necesario asentar la calificacion en la boleta
			# 1.- Hacer la consulta para saber que curso le corresponde al alumno
			# 2.- En el curso correspondiente se debe de verificar dos cosas:
			#     2.1.- Verificar si la materia ya esta dada de alta en la boleta.
			#     2.2.- Verificar que el alumno no tenga mas de tres intentos.
			# 3.- Asentar la calificacion en la boleta
			################################################
			curso = queryset[0].curso # punto 1 cumplido.
			print('EL CONTENIDO DEL CURSO ES:')
			curso = curso
			print(curso,curso.materias.all())
			boleta = str(curso.boleta)

			print('EL CONTENIDO DE LA BOLETA ESSSS:')
			print(boleta.split('\n'))
			print(boleta.split('\r'))
			boletaNueva = rut.agrega_calificacion(boleta.split('\n'),materia,calif,cadenaRespuestas)
			print('Boleta antigua',boleta)
			print('SEPARADOR ENTRE BOLETAS')
			print('Boleta Nueva',boletaNueva)
			if boletaNueva == -1:
				context = {
					'titulo': "NO MAS INTENTOS",
					'mensaje': "Solo se permiten tres evaluaciones por materia",
				}

				return render(request, 'msg_registro_inexistente.html',context)

			Curso.objects.filter(pk=curso.pk).update(boleta=boletaNueva)
			return HttpResponseRedirect("/alumnos")
			return render(request,'impresion_lista_2d.html',context)
	else:
		alumnos = Estudiante.objects.filter(id = alumno)
		if len(alumnos)==0:
			print('NO EXISTE ESE ALUMNO')
			return render(request, 'msg_registro_inexistente.html')
		alumno_str = alumnos[0]
		materias = Materia.objects.filter(id=materia)
		materia_str = materias[0].nombre
		curso = Curso.objects.get(estudiante = alumnos)
		boleta=curso.boleta
		print("El contenido de la coleta essss:",boleta.split('\n'))
		materiaEncontrada= 0
		for linea in boleta.split('\n'):
			if len(linea)!=0 : # si la linea contiene informacion
				print('La linea contiene',linea)
				mat = linea.split()[0]
				print('La materia en la boleta es',mat,' la materia en la consulta es ',materia)
				if int(mat)==int(materia):
					respuestasDesencriptadas = rut.desencripta(linea.split()[-1])
					materiaEncontrada = 1
					break
		respuestasDict = {}
		cnt = 1
		if materiaEncontrada==1:
			for i in respuestasDesencriptadas:
				cadena = 'pregunta_'+str(cnt)
				respuestasDict[cadena] = i
				cnt+=1
		respuestasDict["numero_de_preguntas"] = materias[0].banco.numero_de_reactivos
		if materias[0].banco.preguntas_en_el_mismo_orden ==True:
			respuestasDict["clave_del_examen"] = "0111"
		else:
			respuestasDict["clave_del_examen"] = "1111"
		if materiaEncontrada==1:
			form = preguntas_form(initial=respuestasDict)
		else:
			form = preguntas_form()
		context = {
		"mensaje": "Ingresa la informacion correspondiente",
		"form":form,
		"alumno":alumno_str,
		"materia":materia_str,
		}
	return render(request, "formulario1.html", context)
def evaluacion_digital2(request,alumno,materia):
	""" This function get the answers from the test-form and return the corresponding grade


	"""
	if request.method == 'POST':
		form = preguntas_form(request.POST)
		if form.is_valid():
			queryset = Estudiante.objects.filter(id = alumno)
			if len(queryset)==0:
				print('NO EXISTE ESE ALUMNO')
				return render(request, 'msg_registro_inexistente.html')
			nombre = str(queryset[0])
			claveAlumno = str(queryset[0].numero_de_control)
			#nombre = form.cleaned_data['nombre']
			#claveAlumno = form.cleaned_data['clave_de_alumno']
			numeroPreguntas = form.cleaned_data['numero_de_preguntas']
			claveExamen = form.cleaned_data['clave_del_examen']
			#versionExamen = form.cleaned_data['version_examen']
			listaRespuestas = []
			cadenaRespuestas = ""
			for i in range(1,int(numeroPreguntas)+1):
				cadenaPregunta = 'pregunta_%d'%i
				valor = form.cleaned_data[cadenaPregunta]
				if valor == '':
					calor = -1
				else:
					valor=int(valor)
				listaRespuestas.append(valor)
				cadenaRespuestas += str(valor)
			print("respuestas enviadas son:" ,cadenaRespuestas)
			encriptado = rut.encripta(cadenaRespuestas)
			print("respuestas encriptadas son:" ,encriptado)
			print('Las respuestas desencriptadas son:',rut.desencripta(encriptado))
			#print(nombre,claveAlumno,numeroPreguntas,claveExamen)
			datos = {'nombre':nombre,
			'claveAlumno':claveAlumno,
			'numeroPreguntas':numeroPreguntas,
			'claveExamen':claveExamen,
			'listaRespuestas':listaRespuestas,
			}
			calif,incorr,correc,noContestadas= rut.evaluacionDigital(nombreAlumno=nombre,claveAlumno= claveAlumno,claveExamen = claveExamen,versionExamen=2017,nPreguntas=numeroPreguntas,materia="Aqui va una materia",listaPreguntas=listaRespuestas)
			#return generate_csvFile(request,datos)
			queryset2 = Materia.objects.filter(id=materia)
			materiaNombre = queryset2[0].nombre
			lista = [
			["Nombre del alumno: ",nombre],
			["Folio del alumno: ",claveAlumno],
			["Materia: ",materiaNombre],
			["Calificacion",calif],
			["Incorrectas contestadas por el alumno(%d)"%(len(incorr)),incorr],
			["Correctas (%d)"%(len(correc)),correc],
			["Sin contestar (%d)"%(len(noContestadas)),noContestadas]
			]
			context={
				'mensaje': "El resultado de la evaluacion es:",
				'lista':lista,
			}
			# ahora que se ha evaluado el examen es necesario asentar la calificacion en la boleta
			# 1.- Hacer la consulta para saber que curso le corresponde al alumno
			# 2.- En el curso correspondiente se debe de verificar dos cosas:
			#     2.1.- Verificar si la materia ya esta dada de alta en la boleta.
			#     2.2.- Verificar que el alumno no tenga mas de tres intentos.
			# 3.- Asentar la calificacion en la boleta
			################################################
			curso = queryset[0].curso # punto 1 cumplido.
			print('EL CONTENIDO DEL CURSO ES:')
			curso = curso
			print(curso,curso.materias.all())
			boleta = str(curso.boleta)

			print('EL CONTENIDO DE LA BOLETA ESSSS:')
			print(boleta.split('\n'))
			print(boleta.split('\r'))
			boletaNueva = rut.agrega_calificacion(boleta.split('\n'),materia,calif,cadenaRespuestas)
			print('Boleta antigua',boleta)
			print('SEPARADOR ENTRE BOLETAS')
			print('Boleta Nueva',boletaNueva)
			if boletaNueva == -1:
				context = {
					'titulo': "NO MAS INTENTOS",
					'mensaje': "Solo se permiten tres evaluaciones por materia",
				}

				return render(request, 'msg_registro_inexistente.html',context)

			Curso.objects.filter(pk=curso.pk).update(boleta=boletaNueva)

			return render(request,'impresion_lista_2d.html',context)
	else:
		alumnos = Estudiante.objects.filter(id = alumno)
		if len(alumnos)==0:
			print('NO EXISTE ESE ALUMNO')
			return render(request, 'msg_registro_inexistente.html')
		alumno_str = alumnos[0]
		materias = Materia.objects.filter(id=materia)
		materia_str = materias[0].nombre
		curso = Curso.objects.get(estudiante = alumnos)
		boleta=curso.boleta
		print("El contenido de la coleta essss:",boleta.split('\n'))
		materiaEncontrada= 0
		for linea in boleta.split('\n'):
			if len(linea)!=0 : # si la linea contiene informacion
				print('La linea contiene',linea)
				mat = linea.split()[0]
				print('La materia en la boleta es',mat,' la materia en la consulta es ',materia)
				if int(mat)==int(materia):
					respuestasDesencriptadas = rut.desencripta(linea.split()[-1])
					materiaEncontrada = 1
					break
		respuestasDict = {}
		cnt = 1
		if materiaEncontrada==1:
			for i in respuestasDesencriptadas:
				cadena = 'pregunta_'+str(cnt)
				respuestasDict[cadena] = i
				cnt+=1
		if materiaEncontrada==1:
			form = preguntas_form(initial=respuestasDict)
		else:
			form = preguntas_form()
		context = {
		"mensaje": "Ingresa la informacion correspondiente",
		"form":form,
		"alumno":alumno_str,
		"materia":materia_str,
		}
	return render(request, "formulario1.html", context)
def index_original(request):
	#return render(request, 'index.html', {})
	return render(request,'menuOpcionesAcceso.html',{})
def consultas(request):
	if request.user.is_authenticated():
		return render(request, 'index.html', {})
	else:
		context = {
			'titulo': "Entra primero a tu cuenta en admin",
			'mensaje': "Para poder acceder a esta seccion debes de entrar primero en tu cuenta de admin",
		}

		return render(request, 'msg_registro_inexistente.html',context)
def registro_inexistente(request):
	return render(request, 'msg_registro_inexistente.html')
def accesoAlumno(request):
	if request.method == 'POST':
		form = form_acceso_alumno(request.POST)
		if form.is_valid():
			numero = form.cleaned_data['numero_de_alumno']
			clave = form.cleaned_data['clave_de_alumno']
			print('FORMULARIO ACCESO ALUMNOS')
			print("alumno",numero,'clave',clave)

			queryset = Estudiante.objects.filter(id = numero)
			if len(queryset)==0:
				context = {
					'titulo': "Registro inexistente",
					'mensaje': "Ese alumno no existe en la base de datos",
				}

				return render(request, 'msg_registro_inexistente.html',context)
			else:
				contrasena = queryset[0].contrasena
				print(contrasena)
				if contrasena!=clave:
					context = {
					'titulo': "Informacion invalida",
					'mensaje': "La contrasena o el id no es correcto",
					}

					return render(request, 'msg_registro_inexistente.html',context)
				#cursos = queryset[0].cursos.all()
				#print("Los cursos del alumno son: ",cursos)
				#if len(cursos)==0:
				#	print("No tiene ningun servicio activado este alumno")
				#	context={
				#		"msg":"No tienes ningun curso dado de alta!!!"
				#	}
				#	return render(request, 'msg_registro_inexistente.html',context)
				#print(queryset)
			#index = len(cursos)-1
			# si un alumno tiene varios cursos
			queryset2 = Curso.objects.filter(estudiante=numero)
			if len(queryset2)==0:
				context = {'titulo': 'REGISTRO INVALIDO',
						   'mensaje': 'El alumno no tiene ningun curso dado de alta'}
				return render(request, 'msg_registro_inexistente.html',context)
			print('Las materias del alumno son: ',queryset2)
			print(queryset2[0].materias.all())
			materias = []
			boleta = queryset2[0].boleta
			lineas = []
			cadena = ''
			caracter = ''
			print('La boleta contiene:',boleta)
			for caracter in boleta:
				cadena += caracter
				if caracter =='\n':
					lineas.append(str(cadena[:-1]))
					cadena = ''
			cadena += caracter
			lineas.append(str(cadena[:-1]))
			boleta = lineas
			print('La boleta contiene:',boleta)
			for item in queryset2[0].materias.all():

				claveMateria = str(item).split(":")[0]
				print('\nLa materia que se esta analizando es: ',claveMateria)
				#print(item,claveMateria)
				# send the claveMateria alogn with the alumno id
				periodoValido = timedelta(days=10)
				fechaLimite = periodoValido+item.fecha_termino
				#print('La fecha limite es: ',fechaLimite)
				etiqueta = ''
				link = ''

				print('La fecha limite para aplicar examen: ',fechaLimite)
				#print('La fecha de hoy: ',timezone.localtime(datetime.datetime.now()))
				hoy = timezone.localtime(timezone.now()).date()
				if fechaLimite < hoy:
					# si la fecha de evaluacion digital ya caduco
					print("Ya caduco el examen")
					etiqueta = 'Fuera de fechas, '
					habilitaLink = 0
				else:
					print("Aun es valida la fecha el examen")
					habilitaLink = 1
				#Ahora buscamos la materia en la boleta y verificamos el numero de intentos
				#print("La boleta del alumno es: ", boleta)
				intentos = 0
				for linea in boleta:
					if len(linea)<=1:
						continue
					#print("la linea de la boleta contiene: ", linea)
					mat = linea.split()[0]

					if int(mat) == int(claveMateria):
						intentos = len(linea.split())-2
						print('coincidieron la materia ',int(mat), ' con ',int(claveMateria), intentos)
						if intentos >= 3:
							print('Ya no tiene mas intentos')
							etiqueta += 'sin mas intentos'
							habilitaLink = 0
							break
						else:
							print('Todavia tiene mas intentos, ha hecho ',intentos,' intentos')
							habilitaLink = 1
							if fechaLimite < datetime.datetime.now().date() :
								# si la fecha de evaluacion digital ya caduco
								print("Ya caduco el examen")
								etiqueta = 'Fuera de fechas, '
								habilitaLink = 0
							else:
								print("Aun es valida la fecha el examen")
								habilitaLink = 1
							break
				if habilitaLink==1:
					link = 'eval/' + str(numero) + "/"+str(claveMateria)
				
				if intentos>=1:
					linkEvaluacion = "respuestas/" + str(item.id)
				else:
					linkEvaluacion =""
				if item.fecha_inicio <= hoy and item.fecha_termino >= hoy and item.banco.disponible_para_alumno==True:
					linkMaterial = "archivoPDF/%d/%d"%(int(numero),item.id)
				else:
					linkMaterial = ""

				materias.append([item,intentos,link,etiqueta,linkEvaluacion,linkMaterial])
			#queryset = queryset.filter(creacion_de_registro__gt = fecha1)
			#context = {"queryset":queryset,}
			index = str(queryset[0].Aspirante).find(' ')
			if index == -1:
				index = 0
			nombreAlumno=str(queryset[0].Aspirante)[index:]
			################## Seccion de informacion de la boleta #################

			alumno = numero
			# verificamos que este alumnol exista
			try:
				queryset = Estudiante.objects.get(id = alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'No existe ese alumno en la base de datos',}
				return render(request, 'msg_registro_inexistente.html',context)
			# ahora imprimimos el contenido de su boleta, pero verificamos que si tenga un curso activo.
			try:
				curso = Curso.objects.get(estudiante = alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'El alumno ' + str(queryset) +' no tiene ningun curso registrado',}
				return render(request, 'msg_registro_inexistente.html',context)

			boleta = str(curso.boleta)
			#print("La boleta contiene:\n",boleta)
			calificaciones = []
			for item in boleta.split('\n'):
				if len(item)>1:
					materia = item.split()[0]
					try: # buscamos la materia correspondiente en la base de datos
						queryset = Materia.objects.get(id = materia)
					except ObjectDoesNotExist:
						context = {'mensaje': 'Ocurrio un problema con la base de datos, notificar al desarrollador',}
						return render(request, 'msg_registro_inexistente.html',context)
					lista = [str(queryset.id) + ' ' + queryset.nombre]+['-']*4
					# llenamos las calificaciones correspondientes a cada intento
					for i in range(len(item.split())-2):
						if i<4:
							lista[i+1]=item.split()[i+1]
					calificaciones.append(lista)
			#messages.add_message(request, messages.INFO, 'Se ha actualizado la boleta de manera correcta!')


			########################################################################


			context = {'numero':numero,
			'clave':clave,
			'nombre': nombreAlumno,
			'materias': materias,
			'encabezados': ['Materia', 'Intentos', 'Link',"Evaluacion"],
			'encabezados2': ['Materia', '1ra','2da','3ra','extra'],
			'filas': calificaciones,
			}


			request.session['id_alumno'] = numero
			return render(request,"menu_alumno.html", context)

	else:
		form = form_acceso_alumno()
		context = {
		"mensaje": "Ingresa los datos",
		"form":form,
		}
	#return render(request, "formulario_fechas.html", context)
	return render(request, 'form_acceso_alumno.html', context)
def inscritos_promotor(request):
	idPromotor = int(request.session['idPromotor'])
	queryset = Empleado.objects.filter(id = idPromotor)
	if len(queryset)==0:
		context = {
		'titulo': 'Registro inexistente',
		'mensaje': 'La contrasena o el numero de promotor son incorrectos',}
		return render(request, 'msg_registro_inexistente.html')

	inscritos = Estudiante.objects.filter(Aspirante__promotor = queryset[0])
	print('Los incsritos son: ',inscritos)
	context = {
	'nombre': queryset[0],
	'inscritos': inscritos,
	}
	return render(request,"inscritos_promotor.html", context)

def prospectos_promotor(request):
	idPromotor = int(request.session['idPromotor'])
	queryset = Empleado.objects.filter(id = idPromotor)
	if len(queryset)==0:
		print('NO EXISTE ESE PROMOTOR en la consulta de prospectos')
		context = {
		'titulo': 'Registro inexistente',
		'mensaje': 'La contrasena o el numero de promotor son incorrectos',}
		return render(request, 'msg_registro_inexistente.html')

	prospectos = Aspirantes.objects.filter(promotor = queryset[0])
	#print("Los prospectos del promotor son: ",prospectos)
	if len(prospectos)==0:
		print("No tiene ningun prospecto")
		context={
			"msg":"No tienes ningun prospecto registrado!!!"
		}
		return render(request, 'msg_registro_inexistente.html',context)

	context = {
	'nombre': queryset[0],
	'prospectos': prospectos,
	}

	return render(request,"prospectos_promotor.html", context)

def menu_promotor(request):
	if request.method == 'POST':
		form = form_acceso_alumno(request.POST)
		if form.is_valid():
			numero = form.cleaned_data['numero_de_alumno']
			clave = form.cleaned_data['clave_de_alumno']

			queryset = Empleado.objects.filter(id = numero)
			if len(queryset)==0:
				print('NO EXISTE ESE PROMOTOR')

				return render(request, 'msg_registro_inexistente.html')
			else:
				contrasena = queryset[0].contrasena
				print(contrasena)
				if contrasena!=clave:
					print('La clave de acceso del promotor es incorrecta')
					return render(request, 'msg_registro_inexistente.html')
			request.session['idPromotor'] = numero
			print("El numero del promotor es: ", request.session['idPromotor'])
			return render(request,"menu_promotor.html")

	else:
		form = form_acceso_alumno()
		context = {
		"mensaje": "Ingresa los datos",
		"form":form,
		}
	#return render(request, "formulario_fechas.html", context)
	return render(request, 'form_acceso_alumno.html', context)

def pagos_proximos(request):
	queryset = EgresoGenerales.objects.filter(proxima_fecha_de_pago__gt = timezone.localtime(timezone.now()))
	suma = 0
	filas =[]
	cnt = 1
	for item in queryset:
		suma = suma + item.monto_futuro_a_cubrir
		filas.append([cnt,item.id,"Gasto general",item.concepto,item.monto,item.proxima_fecha_de_pago])
		cnt += 1
	queryset2 = EgresoNomina.objects.filter(proxima_fecha_de_pago__gt = timezone.localtime(timezone.now()))
	suma2 = 0
	for item in queryset2:
		suma2 = suma2 + item.monto_futuro_a_cubrir
		filas.append([cnt,item.id,"Nomina",item.concepto,item.monto,item.proxima_fecha_de_pago])
		cnt += 1

	context = {
			'mensaje': "Proximos pagos a realizar",
			"submensaje": "Suma total: ${0}".format(suma+suma2),
			'encabezados': ["#","ID","Rubro","Concepto","Monto","Fecha"],
			'filas':filas,
			}
	return render(request, "tabla_general.html", context)
	return render(request,"reporte_tablas.html", context)
	#return render(request,"mensaje_prueba.html", context)
def cobros_diarios(request):
	#queryset = Estudiante.objects.filter(estatus = 0)
	queryset = Estudiante.objects.all()
	var1 = 5
	dict1 = {"var1":5}
	#print("Inicia de consulta")
	#for item in queryset:
	#	print("Del estudiante ", item.Aspirante, " los cursos son:")
	#	for curso in tiem.cursos.all:
	#		print(curso)
	context = {"queryset1":queryset,
	}
	return render(request, 'cobros_diarios.html', context)
def cambiaGuionPorComa(fecha):
	fecha = fecha.str
	cnt = 0
	for letra in fecha:
		if letra=='-':
			fecha[cnt] = ','
		cnt += 1
	print(fecha)
	return fecha
def reporte_inscritos_prospectos_por_fechas(request,year,month,day,year2,month2,day2):

	fecha1 = datetime.datetime(int(year),int(month),int(day))
	fecha2 = datetime.datetime(int(year2),int(month2),int(day2))
	queryset = Aspirantes.objects.filter(creacion_de_registro__lt = fecha2)
	queryset = queryset.filter(creacion_de_registro__gt = fecha1)
	table = AspiranteTable(queryset)
	#table2 = EstudianteTable(Estudiante.objects.all())
	RequestConfig(request).configure(table)
	context = {"queryset":table,
			 	#"queryset2":table2
				}
	return render(request,"reporte_tablas.html", context)
	#return render(request,"mensaje_prueba.html", context)

def reporte_prospectos(request):
	if request.method == 'POST':
		form = rango_fechas_form(request.POST)
		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fecha2 = form.cleaned_data['fecha_final']

			print(fecha1,type(fecha1))
			print('Las pruebas resultaron satisfactorias')
			queryset = Aspirantes.objects.filter(creacion_de_registro__lt = fecha2)
			queryset = queryset.filter(creacion_de_registro__gt = fecha1)
			context = {"queryset":queryset,}
			return render(request,"reporte_prospectos.html", context)

	else:
		form = rango_fechas_form()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)
def reporte_con_servicio(request):
	if request.method == 'POST':
		form = fecha_form(request.POST)
		if form.is_valid():
			fecha = form.cleaned_data['fecha']
			queryset = Curso.objects.filter(fecha_de_termino__gt = fecha)
			#queryset = Estudiante.objects.filter(curso__fecha_de_termino__gt = fecha)
			#queryset = Estudiante.objects.all()
			context = {"queryset":queryset,
						'encabezados': ['Nombre', 'horario', 'fecha de inicio','fecha de termino'],
						'mensaje': 'Estos alumnos estan activos actualmente'}
			#print(queryset)
			#print(queryset[0].Estudiante_set.all())

			return render(request,"reporte_activos.html", context)
	else:
		form = fecha_form()
		context = {
		"mensaje": "Ingresa la fecha, esta servira como filtro para saber que alumnos tendran servicio hasta tal fecha",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)
def captura_calificacion(request):
	if request.method == 'POST':
		form = form_captura_cal(request.POST)
		if form.is_valid():
			materia = form.cleaned_data['materia']
			alumno = form.cleaned_data['alumno']
			calif = form.cleaned_data['calificacion']
			alumno = int(alumno)
			# primero verificamos que ese alumno tiene dada de alta esa materia
			try:
				queryset = Estudiante.objects.get(id = alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'No existe ese alumno en la base de datos',}
				return render(request, 'msg_registro_inexistente.html',context)
			# Luego verificamos que el alumno tenga esa materia dada de alta en su curso
			if not(queryset.curso.materias.filter(id=materia).exists()):
				context = {'mensaje': 'El alumno no tiene registrada esa materia',}
				return render(request, 'msg_registro_inexistente.html',context)
			# actualizamos la calificacion en el curso correspondiente
			curso = Curso.objects.get(estudiante = alumno)
			boleta = str(curso.boleta)
			print('El contenido de la boleta antes de guardarla es:')
			print(boleta)
			boletaNueva = rut.agrega_calificacion(boleta.split('\n'),materia,calif,respuestas='000',force=1)
			if boletaNueva == -1:
				messages.add_message(request, messages.INFO, 'La materia ya contenia la calificacion extra, ya no es posible esitar esta!')
				return HttpResponseRedirect('captura_calificacion')
			else:
				Curso.objects.filter(pk=curso.pk).update(boleta=boletaNueva)
			# si todo se ha verificado correctamente entonces regresamos al menu principal
				messages.add_message(request, messages.INFO, 'Se ha actualizado la boleta de manera correcta!')
			print('El contenido de la boleta despues de guardarla es:')
			print(boletaNueva)
			return HttpResponseRedirect('captura_calificacion')
	else:
		form = form_captura_cal()
		context = {
		"mensaje": "Ingresa los datos correpsondientes.",
		"form":form,
		}
	return render(request, "formulario_captura_calificacion.html", context)
def boleta_alumno(request):
	if request.method == 'POST':
		form = form_boleta_alumno(request.POST)
		if form.is_valid():
			alumno = form.cleaned_data['alumno']
			alumno = int(alumno)
			# verificamos que este alumnol exista
			try:
				queryset1 = Estudiante.objects.get(id = alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'No existe ese alumno en la base de datos',}
				return render(request, 'msg_registro_inexistente.html',context)
			# ahora imprimimos el contenido de su boleta, pero verificamos que si tenga un curso activo.
			try:
				curso = Curso.objects.get(estudiante = alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'El alumno ' + str(queryset1) +' no tiene ningun curso registrado',}
				return render(request, 'msg_registro_inexistente.html',context)

			boleta = str(curso.boleta)
			#print("La boleta contiene:\n",boleta)
			calificaciones = []
			for item in boleta.split('\n'):
				if len(item)!=0:
					materia = item.split()[0]
					try: # buscamos la materia correspondiente en la base de datos
						queryset = Materia.objects.get(id = materia)
					except ObjectDoesNotExist:
						context = {'mensaje': 'Ocurrio un problema con la base de datos, notificar al desarrollador',}
						return render(request, 'msg_registro_inexistente.html',context)
					lista = [str(queryset.id) + ' ' + queryset.nombre]+['-']*4
					# llenamos las calificaciones correspondientes a cada intento
					for i in range(len(item.split())-2):
						if i<4:
							lista[i+1]=item.split()[i+1]
					calificaciones.append(lista)
			#messages.add_message(request, messages.INFO, 'Se ha actualizado la boleta de manera correcta!')
			context = {

			'mensaje': "Boleta del alumno: "+str(queryset1),
			'encabezados': ['Materia', '1ra','2da','3ra','extra'],
			'filas': calificaciones,
			}
			#print(queryset)
			#print(queryset[0].Estudiante_set.all())

			return render(request,"tabla_general.html", context)
	else:
		form = form_boleta_alumno()
		context = {
		"mensaje": "De que alumno quieres consultar la boleta",
		"form":form,
		}
	return render(request, "formulario_captura_calificacion.html", context)
def imprime_material_regulares(request):

	if request.method == 'POST':
		form = fechaPlantel_form(request.POST)
		if form.is_valid():

			plantel = form.cleaned_data['plantel']
			print("Alumnos del plantel ",plantel)
			fecha = form.cleaned_data['fecha']
			diaDeLaSemana = form.cleaned_data['fecha'].weekday()
			print("La impresion",diaDeLaSemana)
			inicio = fecha-timedelta(days=diaDeLaSemana) #+timedelta(days=-7) # el material se imprime con 2 semanas de anticipacion, por lo tanto la consulta se hace a partir de 14 dias despues de hoy
			fin = inicio + timedelta(days=6) # Como la impresion de material se hace cada 14 dias entonces no hay que revisar contabilizar materias que inician despues de 4 semanas
			#qs=Materia.objects.filter(fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
			cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados__lte=0,estudiante__activo=True,estudiante__plantel=plantel)
			#cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados=0,estudiante__activo=True,estudiante__empresa=1)
			cv=cv.distinct() # esta consulta contiene todos los cursos de alumnos regulares que inician materias a partir de hoy y hasta la fecha guardada en fin
			cv = cv.order_by('horario')
			filas = []
			print('Cursos validos')
			print(cv)
			for curso in cv:
				fila =[curso.estudiante,curso.horario,curso.estudiante.numero_de_control]  # el primer elemento de la lista es el estudiante
				materias = Materia.objects.filter(curso=curso,fecha_inicio__gte=inicio,fecha_inicio__lte=fin)
				for mat in materias:
					fila.append(mat.id)
				filas.append(fila)
			context = {
					'titulo': "Material para los alumnos del plantel: %s"%plantel,
					'mensaje': "Materiales a imprimir correspondientes a la semana del %s al %s"%(inicio,fin),
					'encabezados': ['Alumno','horario','Folio', 'materia 1','materia 2','Materia 3'],
					'filas': filas,
					}

			return render(request,"tabla_general.html", context)

	form = fechaPlantel_form()
	context = {
	"mensaje": "Ingresa la fecha, se imprimiran los materiales de la semana correspondiente.",
	"form":form,
	}
	return render(request, "formulario_fechas.html", context)
def imprime_material_irregulares(request):

	if request.method == 'POST':
		form = fechaPlantel_form(request.POST)
		if form.is_valid():

			plantel = form.cleaned_data['plantel']
			print("Alumnos del plantel ",plantel)
			fecha = form.cleaned_data['fecha']
			diaDeLaSemana = form.cleaned_data['fecha'].weekday()
			print("La impresion",diaDeLaSemana)
			inicio = fecha-timedelta(days=diaDeLaSemana) #+timedelta(days=-7) # el material se imprime con 2 semanas de anticipacion, por lo tanto la consulta se hace a partir de 14 dias despues de hoy
			fin = inicio + timedelta(days=6) # Como la impresion de material se hace cada 14 dias entonces no hay que revisar contabilizar materias que inician despues de 4 semanas
			#qs=Materia.objects.filter(fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
			cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados__gt=0,estudiante__activo=True,estudiante__plantel=plantel)
			#cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados=0,estudiante__activo=True,estudiante__empresa=1)
			cv=cv.distinct() # esta consulta contiene todos los cursos de alumnos regulares que inician materias a partir de hoy y hasta la fecha guardada en fin
			cv = cv.order_by('horario')
			filas = []
			print('Cursos validos')
			print(cv)

			for curso in cv:
				fila =[curso.estudiante,curso.horario,curso.estudiante.numero_de_control]  # el primer elemento de la lista es el estudiante
				qs = Tarjeton.objects.get(alumno = curso.estudiante)
				pagos_atrasados = qs.pagos_atrasados
				fila.append(pagos_atrasados)
				materias = Materia.objects.filter(curso=curso,fecha_inicio__gte=inicio,fecha_inicio__lte=fin)
				filas.append(fila)
			context = {
					'titulo': "Alumnos activos con pagos atrasados: %s"%plantel,
					'mensaje': "Correspondientes a la semana del %s al %s"%(inicio,fin),
					'encabezados': ['Alumno','horario','Folio','Atrasos'],
					'filas': filas,
					}

			return render(request,"tabla_general.html", context)
	else:
		form = fechaPlantel_form()
		context = {
		"mensaje": "Ingresa la fecha, esta servira como filtro para saber que alumnos tendran servicio hasta tal fecha",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)
def imprime_material_empresa(request):

	if request.method == 'POST':
		form = empresaFecha_form(request.POST)
		if form.is_valid():

			empresa = form.cleaned_data['empresa']
			fecha = form.cleaned_data['fecha']
			diaDeLaSemana = form.cleaned_data['fecha'].weekday()
			print("La impresion",diaDeLaSemana)
			inicio = fecha-timedelta(days=diaDeLaSemana) #+timedelta(days=-7) # el material se imprime con 2 semanas de anticipacion, por lo tanto la consulta se hace a partir de 14 dias despues de hoy
			fin = inicio + timedelta(days=6) # Como la impresion de material se hace cada 14 dias entonces no hay que revisar contabilizar materias que inician despues de 4 semanas
			#qs=Materia.objects.filter(fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
			cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados=0,estudiante__activo=True,estudiante__empresa=empresa)
			cv=cv.distinct() # esta consulta contiene todos los cursos de alumnos regulares que inician materias a partir de hoy y hasta la fecha guardada en fin
			cv = cv.order_by('horario')
			filas = []
			print('Cursos validos')
			print(cv)
			for curso in cv:
				fila =[curso.estudiante,curso.horario,curso.estudiante.numero_de_control] # el primer elemento de la lista es el estudiante
				materias = Materia.objects.filter(curso=curso,fecha_inicio__gte=inicio,fecha_inicio__lte=fin)
				for mat in materias:
					fila.append(mat.examen.clave_del_examen)
				filas.append(fila)
			context = {
					'titulo': "Material para los alumnos de la empresa: %s"%empresa,
					'mensaje': "Materiales a imprimir correspondientes a la semana del %s al %s"%(inicio,fin),
					'encabezados': ['Alumno','horario','Folio', 'materia 1','materia 2','Materia 3'],
					'filas': filas,
					}

			return render(request,"tabla_general.html", context)
	else:
		form = empresaFecha_form()
		context = {
		"mensaje": "Ingresa la fecha, esta servira como filtro para saber que alumnos tendran servicio hasta tal fecha",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)
def imprime_material_alumno(request):
	diaDeLaSemana = datetime.date.today().weekday()
	inicio = timezone.now()+timedelta(days=diaDeLaSemana) # el material se imprime con 2 semanas de anticipacion, por lo tanto la consulta se hace a partir de 14 dias despues de hoy
	fin = inicio + timedelta(days=6) # Como la impresion de material se hace cada 14 dias entonces no hay que revisar contabilizar materias que inician despues de 4 semanas
	#qs=Materia.objects.filter(fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
	cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados=0)
	cv=cv.distinct() # esta consulta contiene todos los cursos de alumnos regulares que inician materias a partir de hoy y hasta la fecha guardada en fin

	filas = []
	print('Cursos validos')
	print(cv)
	for curso in cv:
		fila =[curso.estudiante,curso.estudiante.numero_de_control] # el primer elemento de la lista es el estudiante
		materias = Materia.objects.filter(curso=curso,fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
		for mat in materias:
			fila.append(mat.examen.clave_del_examen)
		filas.append(fila)
	context = {
			'mensaje': "Materiales a imprimir correspondientes a la semana del %s al %s"%(inicio.date(),fin.date()),
			'encabezados': ['Alumno','Folio', 'materia 1','materia 2','Materia 3'],
			'filas': filas,
			}
	return render(request, "reporta_resultados.html", context)
def resumen_prospectos(request):
	if request.method == 'POST':
		form = rango_fechas_form(request.POST)
		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fecha2 = form.cleaned_data['fecha_final']

			#return render(request,"reporte_tablas.html", context)
			#return HttpResponseRedirect(reverse('reporte_inscritos_prospectos_por_fechas',
			#	kwargs={'year':2000,'month':20,'day':20,'year2':3000,'month2':30,'day2':30}))
			rangoFechas = str(fecha1.year) + '/'
			if fecha1.month<10:
				rangoFechas += '0' + str(fecha1.month) + '/'
			else:
				rangoFechas += str(fecha1.month) + '/'
			if fecha1.day<10:
				rangoFechas += '0' + str(fecha1.day) + '/a/'
			else:
				rangoFechas += str(fecha1.day) + '/a/'

			rangoFechas += str(fecha2.year) + '/'
			if fecha2.month<10:
				rangoFechas += '0' + str(fecha2.month) + '/'
			else:
				rangoFechas += str(fecha2.month) + '/'
			if fecha2.day<10:
				rangoFechas += '0' + str(fecha2.day) + '/'
			else:
				rangoFechas += str(fecha2.day) + '/'

			return HttpResponseRedirect('inscritos_y_prospectos_por_fechas_de/'+rangoFechas)
	else:
		form = rango_fechas_form()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)

def calendario_materias(request):

	diaDeLaSemana = datetime.date.today().weekday()
	inicio = timezone.now()+timedelta(days=diaDeLaSemana) # el material se imprime con 2 semanas de anticipacion, por lo tanto la consulta se hace a partir de 14 dias despues de hoy
	fin = inicio + timedelta(days=6) # Como la impresion de material se hace cada 14 dias entonces no hay que revisar contabilizar materias que inician despues de 4 semanas
	#qs=Materia.objects.filter(fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
	cv = Curso.objects.filter(materias__fecha_inicio__gte=inicio,materias__fecha_inicio__lte=fin,estudiante__tarjeton__pagos_atrasados=0)
	cv=cv.distinct() # esta consulta contiene todos los cursos de alumnos regulares que inician materias a partir de hoy y hasta la fecha guardada en fin

	filas = []
	print('Cursos validos')
	print(cv)
	for curso in cv:
		fila =[curso.estudiante,curso.estudiante.numero_de_control] # el primer elemento de la lista es el estudiante
		materias = Materia.objects.filter(curso=curso,fecha_inicio__gte=inicio,fecha_inicio__lt=fin)
		for mat in materias:
			fila.append(mat.examen.clave_del_examen)
		filas.append(fila)
	context = {
			'mensaje': "Materiales a imprimir correspondientes a la semana del %s al %s"%(inicio.date(),fin.date()),
			'encabezados': ['Alumno','Folio', 'materia 1','materia 2','Materia 3'],
			'filas': filas,
			}
	return render(request, "reporta_resultados.html", context)

def documentacion_incompleta_plantel(request):
	if request.method == 'POST':
		form = form_plantel(request.POST)
		if form.is_valid():
			plantel = form.cleaned_data['plantel']
			cursos = Curso.objects.filter(estudiante__documentacion__documentacion_completa=False,estudiante__activo=True)
			cursos = cursos.filter(estudiante__plantel=plantel,estudiante__empresa=1)
			ordCursos = cursos.order_by('fecha_de_termino')
			filas=[]
			#print(alumnos)
			cnt = 0
			for curso in ordCursos:
				docs = Documentacion.objects.filter(alumno=curso.estudiante)
				presentDocs = docs[0].documentacion_entregada.all()
				print(cnt,presentDocs)

				missingDocs = Documento.objects.exclude(pk__in=presentDocs.values_list('pk', flat=True))
				#missingDocs = presentDocs
				alumno = curso.estudiante
				fechaTermino = curso.fecha_de_termino
				losQueFaltan = ""
				for item in missingDocs:
					losQueFaltan+=str(item)+", "
				fila =[alumno,losQueFaltan[:-2],fechaTermino]
				filas.append(fila)

				cnt += 1
			context = {
					'mensaje': "Documentos que le faltan a los alumnos del plantel: %s"%plantel,
					'submensaje': "%d alumnos tienen documentacion incompleta"%cnt,
					'encabezados': ['Alumno','Faltan','Fin de curso'],
					'filas': filas,
					}
			return render(request, "reporta_resultados.html", context)
	else:
		form = form_plantel()
		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "form_gral.html", context)
def documentacion_incompleta_alumno(request):
	if request.method == 'POST':
		form = form_boleta_alumno(request.POST)
		if form.is_valid():
			alumno = form.cleaned_data['alumno']
			# verificamos que este alumnol exista
			try:
				curso = Curso.objects.get(estudiante=alumno,estudiante__activo=True)
			except ObjectDoesNotExist:
				context = {'mensaje': 'No existe ese alumno en la base de datos o esta inactivo',}
				return render(request, 'msg_registro_inexistente.html',context)

			#cursos = cursos.filter(estudiante__plantel=plantel,estudiante__empresa=1)
			#ordCursos = cursos.order_by('fecha_de_termino')
			filas=[]
			#print(alumnos)
			#cnt = 0
			#for curso in cursos:
			docs = Documentacion.objects.filter(alumno=curso.estudiante)
			presentDocs = docs[0].documentacion_entregada.all()
			#print(cnt,presentDocs)

			missingDocs = Documento.objects.exclude(pk__in=presentDocs.values_list('pk', flat=True))
			#missingDocs = presentDocs
			alumno = curso.estudiante
			fechaTermino = curso.fecha_de_termino
			losQueFaltan = ""
			for item in missingDocs:
				losQueFaltan+=str(item)+", "
			fila =[alumno,losQueFaltan[:-2],fechaTermino]
			filas.append(fila)


			context = {
					'mensaje': "Alumno: %s"%alumno,
					'submensaje': "Le faltan %d documentos"%len(missingDocs),
					'encabezados': ['Alumno','Faltan','Fin de curso'],
					'filas': filas,
					}
			return render(request, "reporta_resultados.html", context)
	else:
		form = form_boleta_alumno()
		context = {
		"mensaje": "Introduce el id del alumno",
		"form":form,
		}
	return render(request, "formulario_captura_calificacion.html", context)
def documentacion_incompleta_empresa(request):
	if request.method == 'POST':
		form = form_empresa(request.POST)
		if form.is_valid():
			empresa = form.cleaned_data['empresa']
			cursos = Curso.objects.filter(estudiante__documentacion__documentacion_completa=False,estudiante__activo=True)
			cursos = cursos.filter(estudiante__empresa=empresa)
			ordCursos = cursos.order_by('fecha_de_termino')
			filas=[]
			#print(alumnos)
			cnt = 0
			for curso in ordCursos:
				docs = Documentacion.objects.filter(alumno=curso.estudiante)
				presentDocs = docs[0].documentacion_entregada.all()
				print(cnt,presentDocs)

				missingDocs = Documento.objects.exclude(pk__in=presentDocs.values_list('pk', flat=True))
				alumno = curso.estudiante
				fechaTermino = curso.fecha_de_termino
				losQueFaltan = ""
				for item in missingDocs:
					losQueFaltan+=str(item.id)+", "

				fila =[alumno,losQueFaltan[:-2],fechaTermino]

				#print(cnt,alumno)
				#cnt+=1
				filas.append(fila)

				cnt += 1
			context = {
					'mensaje': "Documentos que le faltan a los alumnos de la empresa: %s"%empresa,
					'submensaje': "%d alumnos tienen documentacion incompleta"%cnt,
					'encabezados': ['Alumno','Falta','Fin de curso'],
					'filas': filas,
					}
			return render(request, "reporta_resultados.html", context)
	else:
		form = form_empresa()
		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "form_gral.html", context)




def ingresos_del_dia(request):
	pagosAlumnos = PagosAlumno.objects.filter(fecha_pago=datetime.date.today())
	total = 0
	filas = []
	cnt=0
	for pago in pagosAlumnos:
		total += pago.monto
		fila = [pago.fecha_pago,pago.alumno,pago.monto,pago.forma_de_pago,pago.folio]
		cnt += 1
		filas.append(fila)
	context = {
			'mensaje': "Se registraron %d movimientos el dia de hoy"%cnt,
			'submensaje': "La suma de ingresos registrados es de $" + str(total),
			'encabezados': ['Fecha','Pago','Monto','Forma de pago','Folio'],
			'filas': filas,
			}
	return render(request, "reporta_resultados.html", context)
def genera_extraordinario(request):
	if request.method == 'POST':
		form = form_genera_extraordinario(request.POST)
		if form.is_valid():
			alumno = form.cleaned_data['alumno']
			materia = form.cleaned_data['materia']

			return HttpResponseRedirect('/eval/%s/%s'%(alumno,materia))
	else:
		form = form_genera_extraordinario()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "form_gral.html", context)
def buscar_alumno_nombre(request):
	if request.method == 'POST':
		form = form_busca_alumno_nombre(request.POST)
		if form.is_valid():
			nombre = form.cleaned_data['nombre']
			paterno = form.cleaned_data['apellido_paterno']
			materno = form.cleaned_data['apellido_materno']
			qs = Estudiante.objects.filter(Aspirante__nombre = nombre)
			filas = []
			cnt=0
			for est in qs:
				fila = [est,est.contrasena]
				cnt += 1
				filas.append(fila)
			context = {
					'mensaje': "Se encontraron %d estudiantes que coinciden con los criterios de busqueda"%cnt,
					#'submensaje': "La suma de ingresos registrados es de $" + str(total),
					'encabezados': ['Estudiante','Contraseña'],
					'filas': filas,
					}
			return render(request, "reporta_resultados.html", context)

	else:
		form = form_busca_alumno_nombre()

		context = {
		"mensaje": "Buscar alumno por nombre",
		"form":form,
		}
	return render(request, "form_gral.html", context)
def consulta_pagos_alumno(request):
	if request.method == 'POST':
		form = form_boleta_alumno(request.POST)
		if form.is_valid():
			alumno = form.cleaned_data['alumno']

			# verificamos que este alumno exista
			try:
				queryset1 = Estudiante.objects.get(id = alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'No existe ese alumno en la base de datos',}
				return render(request, 'msg_registro_inexistente.html',context)
			# Buscamos el tarjeton asociado a este alumno
			try:
				qs = Tarjeton.objects.get(alumno=alumno)
			except ObjectDoesNotExist:
				context = {'mensaje': 'No existe un tarjeton asociado a este alumno',}
				return render(request, 'msg_registro_inexistente.html',context)
			filas = []
			montoCubierto = 0
			for pago in qs.pagos.all():
				fila = [pago.id,pago.folio,pago.fecha_pago,pago.concepto,pago.monto,pago.bonificacion,pago.forma_de_pago]
				filas.append(fila)
				montoCubierto += pago.monto+pago.bonificacion
			detalles = "El alumno ha cubierto un total de $" +str(montoCubierto) + " pesos, tiene una deuda actualmente de $" + str(qs.deuda_actual) + " pesos, "+ str(qs.pagos_atrasados) + " pagos atrasados y su proxima fecha de pago es el " + str(qs.proxima_fecha_de_pago) + "."
			if qs.monto_cubierto == True:
				detalles += " El tarjeton del alumno indica que ha cubierto totalmente el monto del servicio."
			context = {
			'subtitulo': 'Resumen de pagos del alumno: '+ str(queryset1),
			'encabezados': ['ID pago', 'Folio','Fecha','Concepto','Monto','Bonificacion','Forma de pago'],
			'filas': filas,
			'detalles' : detalles
			}
			#print(queryset)
			#print(queryset[0].Estudiante_set.all())

			return render(request,"tabla_general.html", context)
	else:
		form = form_boleta_alumno()
		context = {
		"subtitulo": "Consulta de pagos de alumno",
		"mensaje": "Ingresa el id del alumno",
		"form":form,
		}
	return render(request, "formulario_captura_calificacion.html", context)
def corte_caja(request):
	if request.method == 'POST':
		form = form_corte_caja(request.POST)
		form.save()
	else:

		try:
			qs = CorteCaja.objects.latest('fecha_de_corte')
		except ObjectDoesNotExist:

			print("No existe ningun corte de caja previo, para el correcto funcionamiento de esta funcion es necesario tener al menos un corte de caja")
			context = {'mensaje': 'No existe un corte de caja previo, deberas ingresarlo de manera manual a la base de datos, consulta el manual de usuario para mayor informacion',}
			return render(request, 'msg_registro_inexistente.html',context)

		inicio = qs.fecha_de_corte
		fin = datetime.datetime.now().date()
		print("Se realiza un corte de caja para el intervalo de tiempo ",inicio,fin)
		pagosAlumnos = PagosAlumno.objects.filter(fecha_pago__lte = fin, fecha_pago__gte = inicio)

		filas = []
		cntIngresos=0

		montoIngresos = 0
		for pago in pagosAlumnos:
			montoIngresos += pago.monto
			fila = [pago.fecha_pago,pago.alumno,pago.monto,pago.forma_de_pago,pago.folio]
			cntIngresos += 1
			filas.append(fila)
		montoEgresos = 0
		cntEgresos = 0
		egresos = EgresoGenerales.objects.filter(fecha__lte = fin, fecha__gte = inicio)
		for egreso in egresos:
			montoEgresos += egreso.monto
			fila = [egreso.fecha,egreso.pago_hecho_a,-egreso.monto,egreso.concepto,egreso.folio_de_recibo]
			cntEgresos += 1
			filas.append(fila)
		egresos = EgresoNomina.objects.filter(fecha__lte = fin, fecha__gte = inicio)
		for egreso in egresos:
			montoEgresos += egreso.monto
			fila = [egreso.fecha,egreso.pago_hecho_a,-egreso.monto,egreso.concepto,egreso.folio_de_recibo]
			cntEgresos += 1
			filas.append(fila)
		montoTotal = montoIngresos - montoEgresos
		form = form_corte_caja(initial = {"folio":"0000","fecha_de_corte":datetime.date.today(),"ingresos":montoIngresos,"egresos":montoEgresos})
		form.fields['fecha_de_corte'].disabled = True
		form.fields['ingresos'].disabled = True
		form.fields['egresos'].disabled = True
		context = {
				'mensaje': "Corte de caja del %s al %s"%(inicio,fin),
				'submensaje': "La suma de los movimientos registrados es de $%s, egresos $%s, ingresos $%s"%(str(montoTotal),str(montoEgresos),str(montoIngresos)),
				'encabezados': ['Fecha','Pago','Monto','Forma de pago','Folio'],
				'filas': filas,
				'form':form,
				}

		return render(request, "corte_caja.html", context)
def cobros_por_vencer(request):
	inicio = datetime.date.today() + timedelta(days=1)
	print("La fecha de inicio para la consulta es ",inicio)
	siguienteMes = inicio.month+1
	siguienteAnio =  inicio.year
	print("mes acutal ",inicio.month," mes siguiente ",siguienteMes)
	if siguienteMes==13:
		siguienteMes = 1
		siguienteAnio += 1
	fin = inicio.replace(day=1,month=siguienteMes,year=siguienteAnio)
	print("La fecha final para hacer la consulta es (pero con dias adicionales): ",fin)
	fin = fin - timedelta(days=1)
	print("La fecha correcta final para hacer la consulta es ",fin)
	qs = Tarjeton.objects.filter(alumno__activo=True,proxima_fecha_de_pago__gte=inicio,proxima_fecha_de_pago__lte=fin)
	total = 0
	filas = []
	cnt = 0
	for tar in qs:
		fila = [tar.alumno,tar.proxima_fecha_de_pago,tar.pago_periodico]
		#fila = [pago.fecha_pago,pago.alumno,pago.monto,pago.forma_de_pago,pago.folio]
		total += tar.pago_periodico
		filas.append(fila)
		cnt += 1
	context = {
			'titulo': 'Ingresos programados',
			'submensaje': "Se tiene programado  %d ingresos en colegiaturas en lo que resta del mes, la suma los ingresos programados es $%s pesos."%(cnt,str(total)),
			'encabezados': ['alumno','Fecha de pago','Monto'],
			'filas': filas,
			}
	return render(request, "reporta_resultados.html", context)
def detalle_pago_alumno(request):
	""" Imprime los pagos que ha hecho el alumno

	"""
	if request.method == 'POST':
		form = form_no_alumno(request.POST)
		if form.is_valid():
			id_alumno = form.cleaned_data['alumno']
			try:
				qs = Tarjeton.objects.get(alumno = id_alumno)
			except:
				context = {
					'titulo': "Error!",
					'mensaje': "No se tiene registro del tarjeton del alumno %d en la base de datos"%id_alumno,
				}
				return render(request, 'msg_registro_inexistente.html',context)
			inicio = qs.fecha_abonos_anticipados
			filas = []
			resumen = []
			cnt=0
			
			opciones= {
				'Semanal':timedelta(days=7),
				'Quincenal':timedelta(days=14),
				'Mensual':timedelta(days=28),
				'Un solo pago':timedelta(days=1),
				'Otro': timedelta(days=30, hours=10),
			}
			monto_cubierto = 0
			pago_colegiaturas =0
			for pago in qs.pagos.all():
				fila = [pago.id,pago.folio,pago.fecha_pago,pago.concepto,"$%1.2f"%pago.monto]
				
				cnt += 1
				filas.append(fila)
				if pago.fecha_pago>=inicio:
					abono = pago.monto+pago.bonificacion
					monto_cubierto += abono
					if pago.concepto != "Inscripcion" and pago.concepto!="Cargo administrativo":
						pago_colegiaturas += abono
			print("### El alumno ha pagado en total: ",monto_cubierto,pago_colegiaturas)
			estatus = "(INACTIVO)"
			if qs.alumno.activo==True:
				estatus = "(ACTIVO)"
			mensaje_principal = "%s %s"%(qs.alumno,estatus)
			
		
				#print("PAGOS HECHOS",qs.pagos.all(),inicio)
			if qs.pago_periodico!=0:
				n_pagos = int(qs.monto_a_pagos/qs.pago_periodico)
			else:
				n_pagos=0
			#print(n_pagos,qs.monto_a_pagos/qs.pago_periodico,qs.monto_a_pagos)
			# filas 3 almacena los pagos hechos desde qs.inicio
			filas3 = []
			primer_pago = qs.inicio
			for i in range(n_pagos):
				filas3.append([i+1,primer_pago+i*opciones[qs.esquema_de_pago],qs.pago_periodico])
			
			# la funcion se~nal que calcula los montos atrasados de los alumnos ha presentado algunas 
			# fallas, por esa razon en este segmento de codigo se vuelve a verificar cuanto debe el alumno
			hoy = timezone.localtime(timezone.now()).date()
			deudaReal = 0
			for i in range(len(filas3)):
				#print(hoy,filas3[i][1])
				if hoy<filas3[i][1]:
					break
				deudaReal += filas3[i][2]
				
			if qs.pago_periodico!=0:
				pagos_atrasados = ceil((deudaReal-pago_colegiaturas)/qs.pago_periodico)
			else:
				pagos_atrasados = 1
			print("### realDeuda ", deudaReal)
			print("### El alumno presenta ",pagos_atrasados,"pagos atrasados",qs.monto_total,monto_cubierto)
			if pagos_atrasados<1:
				submensaje = "El alumno esta al corriente en sus pagos"
				cadena_fecha = "Proxima fecha de pago"
				fecha_proxima = qs.proxima_fecha_de_pago
				if qs.monto_total <= monto_cubierto:
					fecha_proxima = "MONTO TOTAL CUBIERTO"
				else:
					# va al corriente pero no ha pagado todo, sin embargo es posible que este adelantando pagos, 
					# en esos casos el cliente solicito que se calcule de manera correcta cual sera la proxima
					# fecha de pagos en funcion de lo que ya ha pagado.
					print("### El alumno no debe pero no tiene el monto total cubierto, calculando su proxima fecha de pago")
					
					primer_pago = qs.inicio
					if qs.pago_periodico!=0:
						colegiaturasPagadas = int(pago_colegiaturas/qs.pago_periodico)
					else:
						colegiaturasPagadas = 1 
					if colegiaturasPagadas == 0:
						fecha_proxima = filas3[0][1]
					else:
						if len(filas3)==0:
							fecha_proxima = "MONTO TOTAL CUBIERTO"
						else:
							# se le resta 1 en las colegiaturas pagadas para que 
							# corresponda con el indice de la lista
							try: 
								fecha_proxima = filas3[colegiaturasPagadas][1] 
							except:
								fecha_proxima = filas3[colegiaturasPagadas-1][1] 
					print("### El alumno ha cubierto ", colegiaturasPagadas,"colegiaturas")

			else:
				submensaje = "El alumno presenta adeudo (pagos atrasados: %d)"%(pagos_atrasados)
				cadena_fecha = "Ultima fecha que debe cubrir "

				fecha_proxima = qs.proxima_fecha_de_pago-pagos_atrasados*opciones[qs.esquema_de_pago]
				#fecha_proxima = qs.proxima_fecha_de_pago
			#fecha_inicio = qs.fecha_abonos_anticipados
			

			resumen = [ (cadena_fecha,fecha_proxima),
						("Monto total",qs.monto_total),
						("Monto a pagos",qs.monto_a_pagos),
						("Pago periodico",qs.pago_periodico),
						("Fecha programada del primer pago",qs.inicio),
						("Fecha de abonos anticipados",qs.fecha_abonos_anticipados),
						("Monto cubierto actualmente",monto_cubierto)]
			context = {
					'mensaje': mensaje_principal,
					'submensaje': submensaje,
					'filas':resumen,
					'encabezados2': ["Id pago","Folio",'Fecha',"Concepto","Monto"],
					'filas2': filas,
					'encabezados3': ["Pago",'Fecha',"Monto"],
					'filas3': filas3,
					}
			return render(request, "reporta_resultados_pago_alumno.html", context)

	else:
		form = form_no_alumno()

		context = {
		"mensaje": "Buscar alumno por nombre",
		"form":form,
		}
	return render(request, "form_gral.html", context)

def ingresos_por_periodo(request):
	if request.method == 'POST':
		form = rango_fechas_plantel_form(request.POST)
		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fecha2 = form.cleaned_data['fecha_final']
			plantel = form.cleaned_data["plantel"]
			qs = PagosAlumno.objects.filter(alumno__plantel=plantel,fecha_pago__gte = fecha1,fecha_pago__lte=fecha2)

			filas = []
			total = 0
			for pago in qs:
				monto = pago.monto
				total += monto
				fila = [pago.id,pago.fecha_pago,monto,pago.concepto,pago.folio]
				filas.append(fila)


			context = {
					'mensaje': "Resumen de los ingresos para el periodo del %s al %s"%(fecha1,fecha2),
					"submensaje": "La suma de los ingresos asciende a un total de $%s"%total,
					'encabezados': ["Id pago","Fecha",'Monto',"Concepto","Folio"],
					'filas':filas,
					}
			return render(request, "tabla_general.html", context)
	else:
		form = rango_fechas_plantel_form()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)

def egresos_por_periodo(request):
	if request.method == 'POST':
		form = rango_fechas_plantel_form(request.POST)
		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fecha2 = form.cleaned_data['fecha_final']
			plantel = form.cleaned_data["plantel"]
			qs = EgresoGenerales.objects.filter(fecha__gte = fecha1,fecha__lte=fecha2,plantel=plantel)
			filas = []
			total = 0
			for pago in qs:
				monto = pago.monto
				total += monto
				fila = [pago.id,pago.fecha,monto,pago.pago_hecho_a,pago.folio_de_recibo]
				filas.append(fila)

			qs2 = EgresoNomina.objects.filter(fecha__gte = fecha1,fecha__lte=fecha2)#,plantel=plantel)
			print("### LA consulta tiene %d registros"%len(qs2))
			for pago in qs2:
				monto = pago.monto
				total += monto
				fila = [pago.id,pago.fecha,monto,pago.concepto,pago.folio_de_recibo]
				filas.append(fila)
			context = {
					'mensaje': "Resumen de los gastos para el periodo del %s al %s"%(fecha1,fecha2),
					"submensaje": "La suma de los egresos asciende a un total de $%s"%total,
					'encabezados': ["Id pago","Fecha",'Monto',"Concepto","Folio"],
					'filas':filas,
					}
			return render(request, "tabla_general.html", context)
	else:
		form = rango_fechas_plantel_form()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)

def balance_por_periodo(request):
	if request.method == 'POST':
		form = rango_fechas_plantel_form(request.POST)
		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fecha2 = form.cleaned_data['fecha_final']
			plantel = form.cleaned_data["plantel"]
			qs = PagosAlumno.objects.filter(alumno__plantel=plantel,fecha_pago__gte = fecha1,fecha_pago__lte=fecha2)
			qs2 = EgresoGenerales.objects.filter(fecha__gte = fecha1,fecha__lte=fecha2,plantel=plantel)
			ingresos = 0
			egresos = 0
			for pago in qs:
				ingresos += pago.monto
			for pago in qs2:
				egresos += pago.monto

			filas = [[ingresos,egresos,ingresos-egresos]]
			context = {
					'mensaje': "Resumen del balance para el periodo del %s al %s"%(fecha1,fecha2),
					"submensaje": "El balance es de $%s"%(ingresos-egresos),
					'encabezados': ["Ingresos","Egresos","Total"],
					'filas':filas,
					}
			return render(request, "tabla_general.html", context)
	else:
		form = rango_fechas_plantel_form()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)
def datos_alumno(request):

	if request.method == 'POST':
		form = form_no_alumno(request.POST)
		if form.is_valid():
			id_alumno = form.cleaned_data['alumno']
			try:
				qs = Estudiante.objects.get(id=id_alumno)
			except:
				context = {
					'titulo': "Error!",
					'mensaje': "No se tiene registro del alumno %d en la base de datos"%id_alumno,
				}
				return render(request, 'msg_registro_inexistente.html',context)

			filas = [[qs,qs.email,qs.Aspirante.celular,qs.Aspirante.telefono]]
			context = {
					'mensaje': "Datos del alumno",
					#"submensaje":
					'encabezados': ["Nombre","Correo","Celular","Telefono"],
					'filas':filas,
					}
			return render(request, "tabla_general.html", context)
	else:
		form = form_no_alumno()

		context = {
		"mensaje": "Ingresa el ID del alumno",
		"form":form,
		}
	return render(request, "formulario_captura_calificacion.html", context)

def imprime_calendario_materias(request):

	if request.method == 'POST':
		form = rango_fechas_calendario_form(request.POST)

		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fecha2 = form.cleaned_data['fecha_final']
			calendario = form.cleaned_data["calendario"]
			#hora = form.cleaned_data["hora_inicio"]
			horario = form.cleaned_data["horario"]
			qs = Materia.objects.filter(fecha_inicio__gte = fecha1,fecha_termino__lte=fecha2,calendario=calendario,horario=horario)
			filas = []
			cnt = 1
			for materia in qs:
				filas.append([cnt,materia.id,materia.nombre,materia.fecha_inicio,materia.fecha_termino])
				cnt +=1
			context = {
					'mensaje': "Materias para el periodo del %s al %s"%(fecha1,fecha2),
					#"submensaje": "El balance es de $%s"%(ingresos-egresos),
					'encabezados': ["#","Materia ID","Nombre","Inicio","Fin"],
					'filas':filas,
					}
			return render(request, "tabla_general.html", context)

	form = rango_fechas_calendario_form()

	context = {
	"mensaje": "Ingresa la informacion correspondiente",
	"form":form,
	}

	return render(request, "formulario_fechas.html", context)

def generaPDF(request):
	if request.method == 'POST':
		form = form_alumno_materia(request.POST)

		if form.is_valid():
			alumno = form.cleaned_data['numero_del_alumno']
			materia = form.cleaned_data['numero_de_la_materia']
			return genera_archivo_PDF(request,alumno,materia,True)

	form = form_alumno_materia()

	context = {
	"mensaje": "Impresion de material para el alumno",
	"form":form,
	}

	return render(request, "formulario_fechas.html", context)

def calcula_pagos(inicio,fin,primerPago,n_pagos,periodo):
	""" Regresa el numero de veces que un elemento de lista de pagos programados
		cae dentro del periodo de fechas de inicio a fin 
	"""
	
	n = 0
	for i in range(n_pagos):
		fechaIndice = primerPago+i*periodo
		if fechaIndice >= inicio and fechaIndice <=fin:
			n += 1
	return n
def proximas_colegiaturas(request):
	opciones= {
		'Semanal':timedelta(days=7),
		'Quincenal':timedelta(days=14),
		'Mensual':timedelta(days=28),
		'Un solo pago':timedelta(days=1),
		'Otro': timedelta(days=30, hours=10),
	}
	if request.method == 'POST':
		form = rango_fechas_plantel_form(request.POST)
		if form.is_valid():
			fecha1 = form.cleaned_data['fecha_inicial']
			fin = form.cleaned_data['fecha_final']

			if fecha1 <=  timezone.localtime(timezone.now()).date():
				inicio = timezone.localtime(timezone.now()).date()
			if fin<=fecha1:
				fin = timezone.localtime(timezone.now()).date()
			plantel = form.cleaned_data["plantel"]
			# consulta que regresa a todos los alumnos activos que no han cubierto
			# el monto total del servicio
			qs = Tarjeton.objects.filter(alumno__activo = True, monto_cubierto=False)
			filas = []
			total = 0
			for tarjeton in qs:
				deudaAlumno = 0
				if tarjeton.deuda_actual>0:
					deudaAlumno += tarjeton.deuda_actual
				if tarjeton.pago_periodico!=0:
					n_pagos = int(tarjeton.monto_a_pagos/tarjeton.pago_periodico)
				else:
					n_pagos=0
				if n_pagos==0:
					continue
				periodo = opciones[tarjeton.esquema_de_pago]
				primerPago = tarjeton.inicio
				nPag = calcula_pagos(inicio,fin,primerPago,n_pagos,periodo)
				if nPag==0:
					continue
				deudaAlumno += nPag*tarjeton.pago_periodico
				fila = [tarjeton.alumno,deudaAlumno]
				if deudaAlumno>0:
					filas.append(fila)
				total += deudaAlumno

			
			context = {
					'mensaje': "Pronostico de los ingresos para el periodo del %s al %s"%(inicio,fin),
					"submensaje": "La suma del pronostico de ingresos es $%s"%total,
					'encabezados': ["Alumno",'Monto'],
					'filas':filas,
					}
			return render(request, "tabla_general.html", context)
	else:
		form = rango_fechas_plantel_form()

		context = {
		"mensaje": "Ingresa el rango de fechas",
		"form":form,
		}
	return render(request, "formulario_fechas.html", context)