from django.db import models
from controlescolar.models import Curso, Estudiante
from siad.models import Empleado, FormaDePago, Plantel
from django.utils import timezone
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
	opciones= (
		('Efectivo','Efectivo'),
		('Deposito','Deposito'),
		('Transferencia','Transferencia'),
		('Cheque','Cheque'),
		('Otro', 'Otro'),
	)
	opcionesConcepto = (
		('Inscripcion','Inscripcion'),
		('Colegiatura','Colegiatura'),
		('Cargo administrativo','Cargo administrativo'),
	)
	alumno = models.ForeignKey(Estudiante)
	fecha_pago = models.DateField(default=timezone.now)
	concepto = models.CharField(max_length = 20,choices = opcionesConcepto,default = 'Colegiatura')
	#concepto = models.ForeignKey(Concepto)
	monto = models.DecimalField(max_digits = 7,decimal_places=2,help_text='Aqui ingresa el monto efectivo que el alumno paga a la institucion')
	bonificacion = models.DecimalField(max_digits = 7,decimal_places=2,default=0,help_text = "Aqui ingresa la bonificacion que se le hara al alumno")
	forma_de_pago = models.ForeignKey(FormaDePago)
	folio = models.CharField(max_length = 10,default = '0000')
	cancelado = models.BooleanField(default = False,help_text='Si un pago es cancelado activa esta casilla')
	movimiento_verificado_por_direccion = models.BooleanField(default = False)
	def __str__(self):
		#return str(self.alumno.id) +': ' + str(self.monto)
		return str(self.id)+":" +str(self.concepto)+"" +str(self.monto+self.bonificacion) +":" +str(self.fecha_pago) + "\n"
	class Meta:
		#ordering = ["nombre"]
		verbose_name_plural = "Pagos de alumnos"
class Ingreso(models.Model):
	numero_registro = models.IntegerField()
class EgresoGenerales(models.Model):
	folio_de_recibo = models.IntegerField(help_text='Ingresa el folio del recibo de cotejo')
	plantel = models.ForeignKey(Plantel)
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
		return "%s: %s - %s"%(self.id,self.concepto,self.fecha)
	class Meta:
		#ordering = ["nombre"]
		verbose_name_plural = "Gastos generales"
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
	class Meta:
		#ordering = ["nombre"]
		verbose_name_plural = "Egresos nominas"
class Tarjeton(models.Model):
	opciones= (
			('Semanal','Semanal'),
			('Quincenal','Quincenal'),
			('Mensual','Mensual'),
			('Un solo pago','Un solo pago'),
			('Otro', 'Otro'),
	)
	alumno = models.OneToOneField(Estudiante)
	inicio =  models.DateField(default= timezone.now,help_text='Fecha del primer pago programado, esta fecha sirve para agendar los pagos siguientes')
	descripcion = models.TextField(max_length = 200,help_text='Descripcion breve relativa al tarjeton',blank=True)
	esquema_de_pago = models.CharField(max_length = 20,choices = opciones,default = 'Semanal',help_text='Esquema de pago')
	monto_total = models.DecimalField(max_digits = 7, decimal_places = 2,help_text='Aqui ingresa el monto total del servicio')
	monto_a_pagos =  models.DecimalField(max_digits = 7, decimal_places = 2,help_text='Aqui ingresa el monto que se cubrira en pagos')
	pago_periodico = models.DecimalField(max_digits = 7, decimal_places = 2,help_text='Cuanto pagara en cada semana, quincena o mes')
	monto_cubierto = models.BooleanField(default = False,help_text='Activa esta casilla si el alumno ha cubierto la totalidad del monto')
	pagos = models.ManyToManyField(PagosAlumno,help_text='Estos son los pagos que ha realizado el alumno',blank  = True)
	proxima_fecha_de_pago =  models.DateField(default= timezone.now)
	pagos_atrasados = models.IntegerField(default = 0)
	tarjeton_verificado_por_direccion = models.BooleanField(default = False)
	deuda_actual =  models.DecimalField(max_digits = 7, decimal_places = 2,help_text='Esta es la cantidad de dinero que debe actualmente el alumno',default = 0,blank = True)
	fecha_abonos_anticipados = models.DateField(default= timezone.now,help_text='Solo se tomaran en cuenta los pagos que se hayan hecho desde esta fecha')
	def __str__(self):
		#return self.alumno.Aspirante.nombre + " " + self.alumno.Aspirante.apellido_paterno + " " + self.alumno.Aspirante.apellido_materno
		return str(self.alumno)
	class Meta:
		#ordering = ["nombre"]
		verbose_name_plural = "Tarjetones"
class CorteCaja(models.Model):
	folio = models.CharField(max_length = 10,default = '0000')
	fecha_de_corte = models.DateField(default= timezone.now)
	ingresos =  models.DecimalField(max_digits = 7, decimal_places = 2,help_text = "Suma total de los ingresos")
	egresos =  models.DecimalField(max_digits = 7, decimal_places = 2,help_text='Suma total de los egresos')
	observaciones = models.TextField(max_length = 200,help_text='Descripcion breve del corte de caja',blank=True)
	def __str__(self):
		return str(self.id)+": "+str(self.fecha_de_corte)
	class Meta:
		#ordering = ["nombre"]
		verbose_name_plural = "Cortes de caja"


class IngresoGeneral(models.Model):
	opciones= (
		('Efectivo','Efectivo'),
		('Deposito','Deposito'),
		('Transferencia','Transferencia'),
		('Cheque','Cheque'),
		('Otro', 'Otro'),
	)
	fecha = models.DateField(default=timezone.now)
	concepto = models.CharField(max_length = 100)
	monto = models.DecimalField(max_digits = 7,decimal_places=2)
	forma_de_pago = models.ForeignKey(FormaDePago)
	folio = models.CharField(max_length = 10,default = '0000')
	def __str__(self):
		#return str(self.alumno.id) +': ' + str(self.monto)
		return str(self.id)+":" +str(self.concepto)+"" +str(self.monto) +":" +str(self.fecha_pago) + "\n"
	class Meta:
		#ordering = ["nombre"]
		verbose_name_plural = "Ingresos generales"