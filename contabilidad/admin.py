from django.contrib import admin
from .models import Proveedor, PagosAlumno, Egreso, Egreso_nomina
class PagosAlumnoAdmin(admin.ModelAdmin):
	raw_id_fields = ('curso_a_pagar',)

admin.site.register(Proveedor)
admin.site.register(PagosAlumno,PagosAlumnoAdmin)
admin.site.register(Egreso)
admin.site.register(Egreso_nomina)

