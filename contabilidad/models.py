from django.db import models
from django.utils import timezone
from controlescolar.models import Curso

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
class Egreso(models.Model):
	opcionesConcepto = (
			('Nomina','Nomina'),
			('Servicios generales','Servicios generales (cfe,internet,etc)'),
			('Gastos corrientes','Gastos corrientes (copias, papeleria, ferreteria)'),
			('Otros','Otros')
	)
	numero_registro = models.IntegerField()
	concepto = models.CharField(max_length = 20)
	descripcion = models.CharField(max_length = 100)
	monto = models.DecimalField(max_digits = 7, decimal_places = 2)
	fecha = models.DateField()
	destino = models.ForeignKey(Proveedor)
	factura = models.BooleanField()
	#monto_cubierto = models.DecimalField(max_digits = 7, decimal_places = 2)
	def __str__(self):
		return self.concepto
