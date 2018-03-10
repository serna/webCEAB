from django.contrib import admin
from .models import Estudiante, Materia, Servicio, Curso,  Documentacion
class EstudianteAdmin(admin.ModelAdmin):
#	list_filter = ('plantelRegistro')

	raw_id_fields = ('Aspirante',)
	search_fields = ('Estudiante_id',)
	filter_horizontal = ('cursos',)
	def get_readonly_fields(self, request, obj=None):
		if request.user.is_superuser:
			return []
		if obj: #This is the case when obj is already created i.e. it's an edit
			return ['Aspirante','estatus','fecha_de_registro','plantel','numero_de_control','cursos','empresa','entre_calles','cp','edad','grad_estudios','estado_civil','numero_de_hijos','curp','calle','colonia',]
		else:
			return []
#class BoletaAdmin(admin.ModelAdmin):
#	raw_id_fields = ('alumno',)
	#search_fields = ('alumno__Aspirante__id',)

class DocumentacionAdmin(admin.ModelAdmin):
	raw_id_fields = ('alumno',)
	search_fields = ('alumno_id',)
	filter_horizontal = ('documentacion_entregada',) 
class CursoAdmin(admin.ModelAdmin):
	#raw_id_fields = ('alumno',)
	search_fields = ('id',)
	filter_horizontal = ('materias',) 
	def get_readonly_fields(self, request, obj=None):
		if request.user.is_superuser:
			return []
		if obj: #This is the case when obj is already created i.e. it's an edit
			return ['tipo_de_curso','adeudo','fecha_de_inicio','fecha_de_termino',]
		else:
			return []



admin.site.register(Estudiante,EstudianteAdmin)
admin.site.register(Materia)
admin.site.register(Servicio)
admin.site.register(Curso,CursoAdmin)
#admin.site.register(Boleta,BoletaAdmin)
admin.site.register(Documentacion,DocumentacionAdmin)