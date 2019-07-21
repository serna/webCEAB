from django.core.management.base import BaseCommand, CommandError
from contabilidad.models import Tarjeton
import datetime
class Command(BaseCommand):
	help = "Actualiza el campo de pagos atrasados para todos los alumnos activos"
	def handle(self,*args,**options):
		inicio = datetime.date.today()
		qs = Tarjeton.objects.filter(alumno__activo=True,proxima_fecha_de_pago__lte=inicio)
		print("estudiantes activos",len(qs))
		#for tarjeton in qs:
		#	tarjeton.save()
		ff = open("log.txt","w")
		ff.write("Se actulizo los registros de pagos atrasados en la fecha: %s"%inicio)
		ff.close()