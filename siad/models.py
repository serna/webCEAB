from django.db import models
from django.utils import timezone
#from contabilidad.models import Proveedor
class Horario(models.Model):
	horario = models.CharField(max_length = 30)
	def __str__(self):
		return "%s: %s"%(self.id,self.horario)
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Horarios"
class Plantel(models.Model):
	nombre = models.CharField(max_length = 50)

	rfc = models.CharField(max_length = 20)
	calle = models.CharField(max_length=100)
	colonia = models.CharField(max_length=100)
	ciudad_y_estado = models.CharField(max_length = 50)
	cp = models.CharField(max_length=5)
	email = models.CharField(max_length=50)
	telefono = models.CharField(max_length = 10)
	def __str__(self):
		return self.nombre
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Planteles" 

class Empleado(models.Model):
	nombre = models.CharField(max_length=30)
	contrasena = models.CharField(max_length=20,null = True, default = '0') 
	plantel = models.ForeignKey(Plantel,on_delete=models.CASCADE)
	nombre = models.CharField(max_length=30)
	apellido_paterno = models.CharField(max_length=20)
	apellido_materno = models.CharField(max_length=20)
	telefono = models.CharField(max_length = 10)
	puesto = models.CharField(max_length = 50)
	sueldo = models.DecimalField(max_digits = 7, decimal_places = 2)
	def __str__(self):
		return "%d: %s %s "%(self.pk,self.nombre,self.apellido_paterno)
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Empleados" 

class ContactoEmpresarial(models.Model):
	nombre = models.CharField(max_length=100)
	telefono = models.CharField(max_length=20,default="000 000 0000")
	extension = models.CharField(max_length=10,default = "0000")
	puesto = models.CharField(max_length=50)
	horario = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Contactos empresariales" 

class Empresa(models.Model):
	nombre = models.CharField(max_length=100)
	rfc = models.CharField(max_length = 20)
	calle = models.CharField(max_length=100)
	colonia = models.CharField(max_length=100)
	ciudad_estado = models.CharField(max_length = 100)
	cp = models.CharField(max_length=5)
	email = models.CharField(max_length=50)
	telefono_extension = models.CharField(max_length=50)
	contacto_empresarial = models.ForeignKey(ContactoEmpresarial,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.id) + ": " + str(self.nombre)
class FormaContacto(models.Model):
	forma_contacto = models.CharField(max_length = 50)
	def __str__(self):
		return self.forma_contacto
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Formas de contacto" 
class Documento(models.Model):
	documento = models.CharField(max_length = 50)
	def __str__(self):
		return self.documento
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Documentos" 
class Estatus(models.Model):
	estatus = models.CharField(max_length = 50)
	def __str__(self):
		return self.estatus
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Estatus" 

class Servicio(models.Model):
	servicio = models.CharField(max_length = 50)
	def __str__(self):
		return self.servicio
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Servicios" 
class FormaDePago(models.Model):
	forma_de_pago = models.CharField(max_length = 50)
	def __str__(self):
		return self.forma_de_pago
	class Meta: 
		#ordering = ["nombre"] 
		verbose_name_plural = "Formas de pago" 
class Calendario(models.Model):
	calendario = models.CharField(max_length = 50)
	def __str__(self):
		return self.calendario
#class Concepto(models.Model):
#	concepto = models.CharField(max_length = 50)
#	def __str__(self):
#		return self.concepto
#	class Meta: 
#		verbose_name_plural = "Conceptos" 