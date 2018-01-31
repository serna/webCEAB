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
def calcula_proxima_fecha_pago(inicio,monto,colegiatura,esquema,pagado):
	""" Computes the next date of payment

		inicio [date]: date since it would be computed the payments
		monto [float]: amount of money that has to be pay
		colegiatura [float]: The amoun of money in each payment
		esquema [string]: the number of days between each payment
		pagado [float]: The amount of money the alumn has alredy paid 

		It returns the next date of payment and the number of delayed payments
	"""
	opciones= {
		'Semanal':timedelta(days=30, hours=10),
		'Quincenal':timedelta(days=15),
		'Mensual':timedelta(days=30, hours=10),
		'Un solo pago':timedelta(days=0, hours=10),
		'Otro': timedelta(days=30, hours=10),
	}
	#inicio = date.today()-timedelta(days=8)
	fechaCalculo = date.today()
	pagoPeriodico = colegiatura
	esquema = opciones[esquema]
	#print('La fecha de inicio es:',inicio)
	#print('La fecha de hoy es:',fechaCalculo)
	#print('Han pasado ', fechaCalculo-inicio, ' dias')
	pag = int((fechaCalculo-inicio)/esquema) # pagos que ya tendrian que estar hechos
	#print('Se tendrian que tener registrados ', pag , ' pagos')
	#print('Equivalente a ', pag*pagoPeriodico, ' pesos')

	if pag*pagoPeriodico>pagado:
		# El alumno esta atrasado en pagos, calculamos la ultima fecha en la que debio hacer un pago
		
		pagosHechos = int(pagado/pagoPeriodico)
		print("El alumno tiene pagos atrasados: ", pag-pagosHechos)
		nextDate = inicio+(pagosHechos+1)*esquema
	else:
		# El alumno esta al corriente de sus pagos, calculamos su siguiente fecha de pago
		pagosHechos = int(pagado/pagoPeriodico)
		print('El alumno esta al corriente en sus pagos')
		nextDate = inicio+(pagosHechos+1)*esquema
	return nextDate, pag-pagosHechos

@receiver(post_save, sender = PagosAlumno)
def pago_realizado_signal(sender, instance, **kwargs):
	""" Senal para registrar los pagos en el tarjeton correspondiente

		Cuando se hace un pago a nombre de un alumno, se agrega al tarjeton del alumno correspondiente
	"""
	queryset = Tarjeton.objects.filter(alumno = instance.alumno) 
	# buscamos el tarjeton del alumno correspondiente
	if len(queryset)==0:
		# No existe el tarjeton correspondiente, por lo tanto hay que crearlo
		print("Creando un tarjeton para el alumno",instance.alumno)
		proximaFecha, pagosAtrasados = calcula_proxima_fecha_pago(inicio=date.today(),
			monto=1000,colegiatura=500,esquema='Semanal',pagado=0)
		tarjetonNuevo = Tarjeton(alumno=instance.alumno,
			inicio=date.today(),
			#inicio=timezone.now,
			esquema_de_pago = 'Semanal',
			monto = 1000,
			monto_cubierto = False,
			pago_periodico = 500,
			proxima_fecha_de_pago =  proximaFecha ,
			pagos_atrasados = pagosAtrasados,
			
			)
		tarjetonNuevo.save()
		print(instance)	
		tarjetonNuevo.pagos.add(instance)
		print('Guardando un tarjeton nuevo, creando desde plantilla predefinida')
		#queryset = Tarjeton.objects.filter(alumno = instance.alumno)
	else:
		# if the tarjeton exists
		print("los pagos que ha hecho son: ", queryset[0].pagos)
		pagado = 0
		#for item in  queryset[0].pagos.all():
		#	if item.concepto=='Colegiatura':
		#		pagado+=item.monto
		#print('El alumno ha pagado en colegiaturas: ',pagado)
		colegiaturaPagada = 0
		for item in queryset[0].pagos.all():
			if item.concepto=="Colegiatura":
				pagado += item.monto
			else:
				colegiaturaPagada = item.monto
		print("El alumno ha pagado en colegiaturas: ",pagado)
		proximaFecha, pagosAtrasados = calcula_proxima_fecha_pago(inicio=queryset[0].inicio,
			monto=queryset[0].monto-colegiaturaPagada,
			colegiatura=queryset[0].pago_periodico,
			esquema=queryset[0].esquema_de_pago,
			pagado=pagado)
		tarjetonExistente = Tarjeton(id = queryset[0].id,
			alumno = queryset[0].alumno,
			inicio = queryset[0].inicio,
			esquema_de_pago = queryset[0].esquema_de_pago,
			monto_cubierto = queryset[0].monto_cubierto,
			monto = queryset[0].monto,
			pago_periodico = queryset[0].pago_periodico,
			proxima_fecha_de_pago =  proximaFecha ,
			pagos_atrasados = pagosAtrasados,
			)
			#proxima_fecha_de_pago =  models.DateField(default= timezone.now)


		print('Agregando/actualizando un pago en el tarjeton de un alumno')	
		tarjetonExistente.save()
		tarjetonExistente.pagos.add(instance)
