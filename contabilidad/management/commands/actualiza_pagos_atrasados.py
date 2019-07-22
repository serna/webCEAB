from django.core.management.base import BaseCommand, CommandError
from contabilidad.models import Tarjeton
import datetime, time 
class Command(BaseCommand):
	help = "Actualiza el campo de pagos atrasados para todos los alumnos activos"
	def handle(self,*args,**options):
		inicio = datetime.date.today()
		qs = Tarjeton.objects.filter(alumno__activo=True,proxima_fecha_de_pago=inicio)
		for tarjeton in qs:
			tarjeton.save()

		qs = Tarjeton.objects.get(alumno=1)
		print("Alumno",qs,qs.inicio)
		qs.inicio = inicio
		qs.descripcion = time.asctime()
		qs.save()
		print("Alumno",qs,qs.inicio,qs.descripcion)
		#ff = open("log.txt","w")
		#ff.write("Se actulizo los registros de pagos atrasados en la fecha: %s"%str(inicio)+str(datetime.time)
		#ff.close()