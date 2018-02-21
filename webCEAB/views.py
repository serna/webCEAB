from django.shortcuts import render, get_object_or_404, render_to_response, redirect # is used to looks for the object that is related the call
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
import datetime
from django.core.mail import send_mail
from controlescolar.models import Estudiante, Curso, Materia
from promotoria.models import Aspirantes
from contabilidad.models import EgresoGenerales, EgresoNomina, Tarjeton
from siad.models import Empleado
from .forms import rango_fechas_form, preguntas_form, form_acceso_alumno
from .tables import AspiranteTable, EstudianteTable, PagosProximosTable, PagosProximosNominaTable,PagospendientesTable
import csv
from django_tables2 import RequestConfig
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from .modules import rutinas as rut

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

	queryset = Tarjeton.objects.filter(monto_cubierto = False)
	queryset = queryset.filter()
	table = PagospendientesTable(queryset)
	

	RequestConfig(request).configure(table)

	context = {"queryset":table,
			 	"subtitulo":"Resumen de pagos proximos",
			 	'subtitle1': 'Generales',
			 	'subtitle2': 'La consulta es de:' + str(dias),
				}
	return render(request,"consultaUnaTabla.html", context)
#def index(request):
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
			numeroPreguntas = form.cleaned_data['numero_de_preguntas']
			claveExamen = form.cleaned_data['clave_del_examen']
			#versionExamen = form.cleaned_data['version_examen']
			listaRespuestas = []
			for i in range(1,222):
				cadenaPregunta = 'pregunta_%d'%i
				valor = form.cleaned_data[cadenaPregunta]
				if valor == '':
					calor = -1
				else:
					valor=int(valor)
				listaRespuestas.append(valor)
			#print(listaRespuestas)

			print(nombre,claveAlumno,numeroPreguntas,claveExamen)
			datos = {'nombre':nombre,
			'claveAlumno':claveAlumno,
			'numeroPreguntas':numeroPreguntas,
			'claveExamen':claveExamen,
			'listaRespuestas':listaRespuestas,
			}
			calif,incorr,correc,noContestadas= rut.evaluacionDigital(nombreAlumno=nombre,claveAlumno= claveAlumno,claveExamen = claveExamen,versionExamen=2017,nPreguntas=numeroPreguntas,materia="Aqui va una materia",listaPreguntas=listaRespuestas)
			#print('nnnnnnnnnnnnnnnnnnnnn',calif)
			#return generate_csvFile(request,datos)
			queryset2 = Materia.objects.filter(id=materia)
			materiaNombre = queryset2[0].nombre
			lista = [
			["Nombre del alumno: ",nombre],
			["Materia: ",materiaNombre],
			["Calificacion",calif],
			["Incorrectas",incorr],
			["Correctas",correc],
			["Sin contestar",noContestadas]
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
			curso = queryset[0].cursos.all() # punto 1 cumplido.
			print("El alumno tiene dados de alta n cursos: ",len(curso),curso)
			print('EL CONTENIDO DEL CURSO ES:')
			curso = curso[len(curso)-1]
			#print(curso,curso.materias.all())
			boleta = str(curso.boleta)
			
			print('EL CONTENIDO DE LA BOLETA ESSSS:')
			print(boleta.split('\n'))
			print(boleta.split('\r'))
			boletaNueva = rut.agrega_calificacion(boleta.split('\n'),materia,calif)
			print('Boleta antigua',boleta)
			print('SEPARADOR ENTRE BOLETAS')
			print('Boleta Nueva',boletaNueva)
			Curso.objects.filter(pk=curso.pk).update(boleta=boletaNueva)
			return render(request,'impresion_lista_2d.html',context)
	else:
		queryset = Estudiante.objects.filter(id = alumno)
		if len(queryset)==0:
			print('NO EXISTE ESE ALUMNO')
			return render(request, 'msg_registro_inexistente.html')
		alumno_str = queryset[0]
		queryset2 = Materia.objects.filter(id=materia)
		materia_str = queryset2[0].nombre 
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
	return render(request, 'index.html', {})
def registro_inexistente(request):
	return render(request, 'msg_registro_inexistente.html')
def accesoAlumno(request):
	if request.method == 'POST':
		form = form_acceso_alumno(request.POST)
		if form.is_valid():
			numero = form.cleaned_data['numero_de_alumno']
			clave = form.cleaned_data['clave_de_alumno']
			print('FORMMULARIO ACCESO ALUMNOS')
			print("alumno",numero,'clave',clave)
			
			queryset = Estudiante.objects.filter(id = numero)
			if len(queryset)==0:
				print('NO EXISTE ESE ALUMNO')

				return render(request, 'msg_registro_inexistente.html')
			else:
				cursos = queryset[0].cursos.all()
				print("Los cursos del alumno son: ",cursos)
				if len(cursos)==0:
					print("No tiene ningun servicio activado este alumno")
					context={
						"msg":"No tienes ningun curso dado de alta!!!"
					}
					return render(request, 'msg_registro_inexistente.html',context)
				print(queryset)
			index = len(cursos)-1
			queryset2 = Curso.objects.filter(id=cursos[index].id)

			print('Las materias del alumno son: ')
			print(queryset2[0].materias.all())
			materias = []
			
			for item in queryset2[0].materias.all():
				
				claveMateria = str(item).split(":")[0]
				print(item,claveMateria)
				# send the claveMateria alogn with the alumno id
				link = 'eval/' + str(numero) + "/"+str(claveMateria)
				materias.append([item,claveMateria,link])
			#queryset = queryset.filter(creacion_de_registro__gt = fecha1)
			#context = {"queryset":queryset,}

			context = {'numero':numero,
			'clave':clave,
			'nombre': queryset[0].Aspirante,
			'materias': materias,
			
			}

			return render(request,"menu_alumno.html", context)
			
	else:
		form = form_acceso_alumno()
		context = {
		"mensaje": "Ingresa los datos",
		"form":form,
		}
	#return render(request, "formulario_fechas.html", context)
	return render(request, 'form_acceso_alumno.html', context)

def pagos_proximos(request):
	queryset = EgresoGenerales.objects.filter(proxima_fecha_de_pago__gt = timezone.now())
	suma = 0
	for item in queryset:
		suma = suma + item.monto_futuro_a_cubrir
	queryset2 = EgresoNomina.objects.filter(proxima_fecha_de_pago__gt = timezone.now())
	suma2 = 0
	for item in queryset2:
		suma2 = suma2 + item.monto_futuro_a_cubrir
	table = PagosProximosTable(queryset)
	table2 = PagosProximosNominaTable(queryset2)

	RequestConfig(request).configure(table)
	RequestConfig(request).configure(table2)
	context = {"queryset":table,
				'queryset2':table2,
			 	"subtitulo":"Resumen de pagos proximos",
			 	"info": 'La deuda futura es de: ' + str(suma+suma2),
			 	'subtitle1': 'Generales',
			 	'subtitle2': 'Nomina',
				}
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

	