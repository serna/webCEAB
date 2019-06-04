from django.db.models.signals import post_save, pre_save,m2m_changed
from django.dispatch import receiver
from .models import PagosAlumno, Tarjeton
from controlescolar.models import Curso
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta,date
import time


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
		if pago.concepto=='Colegiatura' and pago.fecha_pago >= instance.inicio:
			print(pago)
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
	deudaUnSoloPago = 0
	if instance.esquema_de_pago=='Un solo pago':
		print("El alumno pago el servicio en una sola exhibicion")
		for pago in instance.pagos.all():
			if pago.concepto=='Inscripcion':
				montoCubierto += pago.monto + pago.bonificacion
		if montoCubierto < instance.monto_total:
			# si el alumno no ha cubierto el total del servicio
			deudaUnSoloPago = instance.monto_total-montoCubierto
			instance.pagos_atrasados = 1
			instance.deuda_actual = deudaUnSoloPago
			instance.proxima_fecha_de_pago = date.today()
			instance.monto_cubierto=False
			print("El alumno no cubrio el monto total del servicio con los pagos que tiene registrados, debe: ",deudaUnSoloPago)
			return 0
		else:
			print("El alumno ha cubierto la totalidad del servicio")
			instance.pagos_atrasados = 0
			instance.deuda_actual = deudaUnSoloPago
			instance.proxima_fecha_de_pago = date.today()
			instance.monto_cubierto=True
			return 0
	nDiasEsquema = opciones[instance.esquema_de_pago]
	if fechaCalculo<instance.inicio:
		nPag = -1
	else:
		nPag = int((fechaCalculo-instance.inicio)/nDiasEsquema)+1 # pagos que ya tendrian que estar hechos
	print("Calculo de pagos",int((fechaCalculo-instance.inicio)/nDiasEsquema))
	if instance.pago_periodico!=0:
		if nPag>instance.monto_a_pagos/instance.pago_periodico:
			# dado que nPag es calculado con la fecha actual, es posible que nPag sea mayor
			# que el numero de pagos efectivos que el alumno deberia haber hecho, es decir,
			# el sistema pudiera estar reportando que debe 10 pagos cuando en realidad con
			# 7 pagos el alumno ya habria cubierto su deuda, esto se debe a que usamos la fecha actual
			# para calcular el numero de pagos que deberia de tener hechos el alumno,
			# esta condicion resuelve parcialmente este problema (lo resuelve parcialmente porque
			# hay una ambiguedad entre monto total y monto a pagos que pudiera llevar a algun error)
			nPag = int(instance.monto_a_pagos/instance.pago_periodico)
	else:
		nPag=15 # 
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
	if deuda<=0:
		instance.monto_cubierto = True
	else:
		instance.monto_completo = False
	# Ahora calculamos la siguiente fecha de pago
	instance.proxima_fecha_de_pago = instance.inicio+(pagosHechos)*opciones[instance.esquema_de_pago]


	
		


