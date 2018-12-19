from django.db.models.signals import post_save, pre_save,m2m_changed
from django.dispatch import receiver
from .models import PagosAlumno, Tarjeton
from controlescolar.models import Curso
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta,date
import time
#@receiver(pre_save, sender=PagosAlumno)
#def my_handler(sender,instance,**kwargs):
#	if not(instance.id):
		#print(instance.monto)
		#print(instance.curso_a_pagar)
		#print(instance.curso_a_pagar.id)
#		try:
#			obj = Curso.objects.get(id=instance.curso_a_pagar.id)
#			obj.adeudo -= instance.monto
#			obj.save()
#		except Curso.DoesNotExist:
#			print("No se pudo realizar la operacion de actualizar el monto")
#		print(obj)
def calcula_proxima_fecha_pago(inicio,montoTotal,monto,colegiatura,esquema,pagado):
	""" Computes the next date of payment

		inicio [date]: date since it would be computed the payments
		monto [float]: amount of money that has to be paid
		colegiatura [float]: The amoun of money in each payment
		esquema [string]: the number of days between each payment
		pagado [float]: The amount of money the alumno has alredy paid 

		It returns the next date of payment and the number of delayed payments
	"""
	opciones= {
		'Semanal':timedelta(days=7, hours=1),
		'Quincenal':timedelta(days=14),
		'Mensual':timedelta(days=28, hours=1),
		'Un solo pago':timedelta(days=0, hours=10),
		'Otro': timedelta(days=30, hours=10),
	}
	#inicio = date.today()-timedelta(days=8)
	unSoloPago = 0
	#print('El esquema de pago es: ',esquema)
	if esquema=='Un solo pago':
		#print('EEEEEEEl esquema de pago es: ',esquema)
		unSoloPago=1
	fechaCalculo = date.today()
	pagoPeriodico = colegiatura
	esquema = opciones[esquema]
	#('La fecha de inicio es:',inicio)
	#print('La fecha de hoy es:',fechaCalculo)
	#print('Han pasado ', fechaCalculo-inicio, ' dias')
	nPag = int((fechaCalculo-inicio)/esquema)+1 # pagos que ya tendrian que estar hechos
	#print('Se tendrian que tener registrados 1 ', nPag , ' pagos')
	if unSoloPago==1:
		nPag = 1
		pagoPeriodico = montoTotal
		#print('Se tendrian que tener registrados 2 ', nPag , ' pagos')

	#if nPag>montoTotal/pagoPeriodico:
		#nPag = int(round(montoTotal/pagoPeriodico))
		#print('Se tendrian que tener registrados 3 ', nPag , ' pagos')
	#print('Se tendrian que tener registradossssss ', nPag , ' pagos')
	print('Equivalente a ', nPag*pagoPeriodico, ' pesos')
	atrasados=-1
	if nPag*pagoPeriodico>pagado: # nPages el numero de pagos que ya deberia de tener hechos el alumno
		# El alumno esta atrasado en pagos, calculamos la ultima fecha en la que debio hacer un pago
		
		pagosHechos = int(pagado/pagoPeriodico)
		atrasados = nPag-pagosHechos
		print("El alumno tiene pagos atrasados: ", nPag-pagosHechos)
		nextDate = inicio+(pagosHechos)*esquema
	else:
		# El alumno esta al corriente de sus pagos, calculamos su siguiente fecha de pago
		print("El pago peridodico esssssssssssssssss",pagoPeriodico)
		pagosHechos = int(pagado/pagoPeriodico)
		print('El alumno esta al corriente en sus pagos')
		#print('pagado',pagado,'pagoPeriodico',pagoPeriodico)
		nextDate = inicio+(pagosHechos+1)*esquema
		print('proxima fecha de pago',nextDate)
		atrasados = 0
	return nextDate,  atrasados

@receiver(post_save, sender = PagosAlumno)
def pago_realizado_signal(sender, instance, **kwargs):
	""" Senal para registrar los pagos en el tarjeton correspondiente

		Cuando se hace un pago a nombre de un alumno, se agrega al tarjeton del alumno correspondiente
	"""
	queryset = Tarjeton.objects.filter(alumno = instance.alumno) 
	# buscamos el tarjeton del alumno correspondiente
	print("Guardando pago")
	if len(queryset)!=0:
		# if the tarjeton exists
		tarjetonExistente = Tarjeton.objects.get(id = queryset[0].id)
		tarjetonExistente.pagos.add(instance) # guardamos el pago recien hecho
		tarjetonExistente.save() # guardamos el tarjeton
		
@receiver(pre_save, sender = Tarjeton)
def actualiza_tarjeton(sender, instance, **kwargs):
	""" Senal para actualizar la deuda actual del alumno y el numero e pagos pendientes

		Cuando se hace un cambio en el tarjeton se debe de verificar que el numero de pagos atra
	"""
	if not(instance.id):
		# si no logramos actualizar el tarjeton que esta por guardarse
		print("No se cumplio la condicion para entrar en la rutina que actualiza el tarjeton")
		return 0
	print("\nEntramos en la rutina para actulizar el tarjeton del alumno  ",instance.alumno)
	montoCubierto = 0
	for pago in instance.pagos.all():
		if pago.concepto=='Colegiatura':
			montoCubierto += pago.monto + pago.bonificacion
	# estas opciones sirven para verificar el periodo de tiempo en el que se deben de realizar los cobros
	opciones= {
		'Semanal':timedelta(days=7),
		'Quincenal':timedelta(days=14),
		'Mensual':timedelta(days=28),
		'Un solo pago':timedelta(days=1),
		'Otro': timedelta(days=30, hours=10),
	}
	fechaCalculo = date.today()
	# dividimos el numero de dias que han pasado desde el primer pago del alumno
	# entre el numero de dias que dura el esquema de pagos del alumno, si el esquema 
	# es en un solo pago, entonces solo se revisa que el alumno haya cubierto el total
	if instance.esquema_de_pago=='Un solo pago':
		print("El alumno pago el servicio en una sola exhibicion")
		for pago in instance.pagos.all():
			if pago.concepto!='Colegiatura':
				montoCubierto += pago.monto + pago.bonificacion
		if montoCubierto < instance.monto_total:
			# si el alumno no ha cubierto el total del servicio
			print("El alumno no cubrio el monto total del servicio con los pagos que tiene registrados")
			instance.pagos_atrasados = 1
			instance.deuda_actual = instance.monto_a_pagos
			return 0
		else:
			print("El alumno ha cubierto la totalidad del servicio")
			return 0
	nDiasEsquema = opciones[instance.esquema_de_pago]
	nPag = int((fechaCalculo-instance.inicio)/nDiasEsquema)+1 # pagos que ya tendrian que estar hechos
	print("El numero de pagos que el alumno deberia tener registrados son: ",nPag,fechaCalculo,instance.inicio,nDiasEsquema)
	pagoPeriodico = instance.pago_periodico
	montoHaCubrir = nPag*pagoPeriodico # esto es lo que deberia de haber ya pagado el alumno

	print("Que corresponde a una cantidad de: ",montoHaCubrir)
	print("El alumno ha cubierto",montoCubierto)
	# ahora calculamos el numero de pagos que se ha atrasado, para ellos solo vemos cuantos pagos_periodicos completos 
	# se necesitan para cubrir su deuda

	if pagoPeriodico != 0:
		pagosHechos = int(montoCubierto/pagoPeriodico) # cuantos pagos completos ha hecho el alumno
		nAtrasos = nPag-pagosHechos # cuantos pagos se ha atrasado, quivalentmente seria pero con la funcion ceiling (montoHaCubrir-montoCubierto)/pagoPeriodico
		print("El alumno se atraso ",nAtrasos," y tiene ",pagosHechos," pagos hechos")
	else:
		# si pagoPeriodico es igual a cero nos indica una situacion anomala, para que el usuario note este error
		# reportaremos, aunque no sea cierto, que este alumno tiene varios atrasos para que llame la atencion al usuario
		pagosHechos = 0
		nAtrasos = 5
	
	deuda = montoHaCubrir-montoCubierto
	instance.deuda_actual = deuda
	instance.pagos_atrasados = nAtrasos

	# Ahora calculamos la siguiente fecha de pago
	instance.proxima_fecha_de_pago = instance.inicio+(pagosHechos)*opciones[instance.esquema_de_pago]


	
		


