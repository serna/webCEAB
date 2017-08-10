from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from siad.models import Plantel, Empleado, Empresa, FormaContacto
from django.core.urlresolvers import reverse
class Aspirantes(models.Model):
	#plantel = models.ForeignKey(Plantel)
	nombre = models.CharField(max_length=30)
	apellido_paterno = models.CharField(max_length=20)
	apellido_materno = models.CharField(max_length=20)
	creacion_de_registro = models.DateField(default=timezone.now)
	promotor = models.ForeignKey(Empleado)
	forma_contacto = models.ForeignKey(FormaContacto)
	telefono = models.CharField(max_length = 10)
	celular = models.CharField(max_length = 13)
	

	class Meta:
		verbose_name_plural = "Prospectos" 
		#ordering=["apellidoPaterno"]

	def __str__(self):
		return "%d %s %s %s" % (self.pk,self.nombre,self.apellido_paterno,self.apellido_materno)
	def get_absolute_url(self):
		return reverse("detalleAspirante", kwargs={"id": self.id})
#class Caracteristica(models.Model):
#	aspirante = models.OneToOneField(Aspirantes,null = True)
#	descripcion = models.CharField(max_length = 20)
#	def __str__(self):
#		return "%s" % (self.aspirante)