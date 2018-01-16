from django.db.models.signals import post_save, pre_save,m2m_changed
from django.dispatch import receiver
from .models import PagosAlumno, Tarjeton
from controlescolar.models import Curso
from django.contrib import messages
from django.utils import timezone
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
		tarjetonNuevo = Tarjeton(alumno=instance.alumno,
			inicio=timezone.now(),
			Esquema_de_pago = 'Semanal',
			monto = 1000,
			monto_cubierto = 0,
			
			)
		tarjetonNuevo.save()
		print(instance)	
		tarjetonNuevo.pagos.add(instance)
		print('Guardando un tarjeton nuevo, creando desde plantilla predefinida')
		#queryset = Tarjeton.objects.filter(alumno = instance.alumno)
	else:
		#print(queryset[0].id)
		tarjetonExistente = Tarjeton(id = queryset[0].id,
			alumno = queryset[0].alumno,
			inicio = queryset[0].inicio,
			Esquema_de_pago = queryset[0].Esquema_de_pago,
			monto_cubierto = queryset[0].monto_cubierto,
			monto = queryset[0].monto)
		print('Agregando/actualizando un pago en el tarjeton de un alumno')	
		tarjetonExistente.save()
		tarjetonExistente.pagos.add(instance)
