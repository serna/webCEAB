from django.contrib import admin
from .models import Proveedor, PagosAlumno, Egreso
class PagosAlumnoAdmin(admin.ModelAdmin):
#	list_filter = ('plantelRegistro')

	raw_id_fields = ('curso_a_pagar',)

admin.site.register(Proveedor)
admin.site.register(PagosAlumno,PagosAlumnoAdmin)
admin.site.register(Egreso)

