from django.contrib import admin
from django.forms import ModelForm
from .models import Proveedor, PagosAlumno, EgresoGenerales, EgresoNomina, Tarjeton, CorteCaja,IngresoGeneral



class IngresoGeneralAdmin(admin.ModelAdmin):
	search_fields = ('id',)
	#def get_form(self, request, obj=None, **kwargs):
	#	if request.user.is_superuser:
	#		kwargs['form'] = EgresoSuperUserForm
	#	else:
	#		kwargs['form'] = EgresoNormalUserForm
	#	return super(EgresoGeneralesAdmin, self).get_form(request, obj, **kwargs)
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = [] # set all fields as editable
		elif obj:
			for f in self.model._meta.fields:
				# et all fields as readoonly for all not superuser
				if f.name != 'id' :
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = []
		return readOnlyFields
admin.site.register(IngresoGeneral,IngresoGeneralAdmin)


class EgresoGeneralesAdmin(admin.ModelAdmin):
	search_fields = ('realizo_pago',)
	#def get_form(self, request, obj=None, **kwargs):
	#	if request.user.is_superuser:
	#		kwargs['form'] = EgresoSuperUserForm
	#	else:
	#		kwargs['form'] = EgresoNormalUserForm
	#	return super(EgresoGeneralesAdmin, self).get_form(request, obj, **kwargs)
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = [] # set all fields as editable
		elif obj:
			for f in self.model._meta.fields:
				# et all fields as readoonly for all not superuser
				if f.name != 'id' :
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = []
		return readOnlyFields
admin.site.register(EgresoGenerales,EgresoGeneralesAdmin)

class EgresoNominasAdmin(admin.ModelAdmin):
	search_fields = ('realizo_pago',)
	#def get_form(self, request, obj=None, **kwargs):
	#	if request.user.is_superuser:
	#		kwargs['form'] = EgresoSuperUserForm
	#	else:
	#		kwargs['form'] = EgresoNormalUserForm
	#	return super(EgresoGeneralesAdmin, self).get_form(request, obj, **kwargs)
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = [] # set all fields as editable
		elif obj:
			for f in self.model._meta.fields:
				# et all fields as readoonly for all not superuser
				if f.name != 'id' :
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = []
		return readOnlyFields
admin.site.register(EgresoNomina,EgresoNominasAdmin)


class PagosAlumnoAdmin(admin.ModelAdmin):
	raw_id_fields = ('alumno',)
	search_fields = ('id',)
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = [] # set all fields as editable
		elif obj:
			for f in self.model._meta.fields:
				# et all fields as readoonly for all not superuser
				if f.name != 'id':
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = ['movimiento_verificado_por_direccion','cancelado']
		return readOnlyFields
admin.site.register(PagosAlumno,PagosAlumnoAdmin)
#admin.site.register(Tarjeton)
class ProveedoresAdmin(admin.ModelAdmin):
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = [] # set all fields as editable
		elif obj:
			for f in self.model._meta.fields:
				# et all fields as readoonly for all not superuser
				if f.name != 'id' :
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = []
		return readOnlyFields
admin.site.register(Proveedor,ProveedoresAdmin)
	
class TarjetonAdmin(admin.ModelAdmin):
	#list_filter = ('plantelRegistro')
	#raw_id_fields = ('Aspirante',)
	search_fields = ('=alumno__id',)
	#filter_horizontal = ('cursos',)
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		print(request.user,type(request.user))
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = ['pagos','pagos_atrasados','proxima_fecha_de_pago','deuda_actual']
		elif obj:
			# if the object is created then make all fields readonly
			for f in self.model._meta.fields:
				# en el siguiente if se enlistan los campos que podra modificar los usuarios
				# que no son superusuarios
				if f.name != 'id'  and f.name != 'monto_cubierto':
					readOnlyFields.append(f.name)
			readOnlyFields.append('pagos')
		else:
			# if the obj is not created then just protect some fields as readonly
			readOnlyFields = ['pagos','tarjeton_verificado_por_direccion','monto_cubierto']
		return readOnlyFields
admin.site.register(Tarjeton,TarjetonAdmin)

admin.site.register(CorteCaja)

