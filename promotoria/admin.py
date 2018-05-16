from django.contrib import admin
from .models import Aspirantes

class AspirantesAdmin(admin.ModelAdmin):
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
	

admin.site.register(Aspirantes,AspirantesAdmin)
#admin.site.register(Caracteristica,CaracteristicaAdmin)
