from django.contrib import admin
from .models import Estudiante, Materia, Servicio, Curso,  Documentacion, Catalogo

admin.site.register(Catalogo)
class CursosAdmin(admin.ModelAdmin):
	filter_horizontal = ('materias',)
	search_fields = ('estudiante__id',)
	def get_readonly_fields(self, request, obj=None):
		# regresa la lista de campos que son de solo lectura
		readOnlyFields = []
		if request.user.is_superuser:
			# habra un usuario, llamado direccion, que puede modificar casi todos los campos
			# sera superusuario, en esta funcion se determina que campos no podra modificar
			readOnlyFields = [] # set all fields as editable
			
		elif obj:
			for f in self.model._meta.fields:
				# et all fields as readoonly for all but superuser
				if f.name != 'id' and f.name != 'materias':
					readOnlyFields.append(f.name)
			
		else:
			readOnlyFields = []
			#readOnlyFields.append('materias')
		#readOnlyFields.append('boleta')
		return readOnlyFields
admin.site.register(Curso,CursosAdmin)

class DocumentacionAdmin(admin.ModelAdmin):
	filter_horizontal = ('documentacion_entregada',)
	search_fields = ('estudiante__id',)
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
				if f.name != 'id' and f.name != 'documentacion_completa':
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = []
		return readOnlyFields
admin.site.register(Documentacion,DocumentacionAdmin)

class EstudianteAdmin(admin.ModelAdmin):
	#filter_horizontal = ('cursos',)
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
				if f.name != 'id' :
					readOnlyFields.append(f.name)
		else:
			readOnlyFields = []
		#readOnlyFields.append('cursos')
		return readOnlyFields
admin.site.register(Estudiante,EstudianteAdmin)

class MateriasAdmin(admin.ModelAdmin):
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
admin.site.register(Materia,MateriasAdmin)





#admin.site.register(Estudiante,EstudianteAdmin)

admin.site.register(Servicio)

#admin.site.register(Boleta,BoletaAdmin)
