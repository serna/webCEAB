from django.contrib import admin
from .models import Aspirantes

class AspirantesAdmin(admin.ModelAdmin):
#	list_filter = ('plantelRegistro')
	#raw_id_fields = ('plantel',)
	search_fields = ('nombre','apellidoPaterno')
#class CaracteristicaAdmin(admin.ModelAdmin):
	#fields = ('aspirante','descripcion',)
#	readonly_fields = ('aspirante',)
	
admin.site.register(Aspirantes,AspirantesAdmin)
#admin.site.register(Caracteristica,CaracteristicaAdmin)
