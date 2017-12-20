from django.db import models
from django.utils import timezone
from controlescolar.models import Curso
from siad.models import Empleado
#import datetime
# Create your models here.
class Proveedor(models.Model):
	nombre = models.CharField(max_length=100)
	rfc = models.CharField(max_length = 20)
	calle = models.CharField(max_length=100)
	colonia = models.CharField(max_length=100)
	ciudad_y_estado = models.CharField(max_length = 100)
	cp = models.CharField(max_length=5)
	email = models.CharField(max_length=50)
	telefono_extension = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Proveedores" 

class PagosAlumno(models.Model):
	#alumno = models.ForeignKey(Alumno)
	#opcionesEsquema = (
	#		('Semanal','Semanal'),
	#		('Quincenal','Quincenal'),
	#		('Mensual','Mensual'),
	#		('Un solo pago','Un solo pago'),
	#		('Otro', 'otro'),
	#)
	#esquema = models.CharField(max_length = 10,choices = opcionesEsquema,default = 'Semanal')
	fecha_pago = models.DateField(default=timezone.now)
	monto = models.DecimalField(max_digits = 7,decimal_places=2)
	curso_a_pagar = models.ForeignKey(Curso)
	def __str__(self):
		return str(self.id) + ": " + str(self.monto)
class Ingreso(models.Model):
	numero_registro = models.IntegerField()
class EgresoGenerales(models.Model):
	folio_de_recibo = models.IntegerField(help_text='Ingresa el folio del recibo de cotejo')
	concepto = models.CharField(max_length = 40)
	descripcion = models.CharField(max_length = 100)
	monto = models.DecimalField(max_digits = 7, decimal_places = 2)
	fecha = models.DateField(default= timezone.now)
	pago_hecho_a = models.ForeignKey(Proveedor)
	factura = models.CharField(max_length = 30)
	proxima_fecha_de_pago =  models.DateField(default= timezone.now)
	monto_futuro_a_cubrir =  models.DecimalField(max_digits = 7, decimal_places = 2)
	realizo_pago = models.ForeignKey(Empleado)
	movimiento_verificado_por_direccion = models.BooleanField(default = False)
	#monto_cubierto = models.DecimalField(max_digits = 7, decimal_places = 2)
	def __str__(self):
		return "%s;\t%s;\t%s"%(self.movimiento_verificado_por_direccion,self.concepto,self.fecha)

class EgresoNomina(models.Model):
	folio_de_recibo = models.IntegerField()
	concepto = models.CharField(max_length = 40)
	monto = models.DecimalField(max_digits = 7, decimal_places = 2)
	fecha = models.DateField(default= timezone.now)
	pago_hecho_a = models.ForeignKey(Empleado)
	proxima_fecha_de_pago =  models.DateField(default= timezone.now)
	monto_futuro_a_cubrir =  models.DecimalField(max_digits = 7, decimal_places = 2)
	#monto_cubierto = models.DecimalField(max_digits = 7, decimal_places = 2)
	def __str__(self):
		return self.concepto