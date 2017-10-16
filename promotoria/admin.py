from django.contrib import admin
from .models import Aspirantes

class AspirantesAdmin(admin.ModelAdmin):
#	list_filter = ('plantelRegistro')
	#raw_id_fields = ('plantel',)
	search_fields = ('nombre','apellidoPaterno')
#class CaracteristicaAdmin(admin.ModelAdmin):
	#fields = ('aspirante','descripcion',)
#	readonly_fields = ('aspirante',)
	def get_readonly_fields(self, request, obj=None):
		if request.user.is_superuser:
			return []
		if obj: #This is the case when obj is already created i.e. it's an edit
			return ['nombre','apellido_paterno','apellido_materno','creacion_de_registro',
			'promotor','forma_contacto','telefono','celular',]
		else:
			return []
	

admin.site.register(Aspirantes,AspirantesAdmin)
#admin.site.register(Caracteristica,CaracteristicaAdmin)
