from django.contrib import admin
from django.forms import ModelForm
from .models import Proveedor, PagosAlumno, EgresoGenerales, EgresoNomina
class PagosAlumnoAdmin(admin.ModelAdmin):
	raw_id_fields = ('curso_a_pagar',)

admin.site.register(Proveedor)
admin.site.register(PagosAlumno,PagosAlumnoAdmin)

admin.site.register(EgresoNomina)

class EgresoNormalUserForm(ModelForm):
	""" Form definition for normal user

		Normal user is not capable of change the movimiento_verificado_por_direccion
		field.
	"""
	class Meta:
		model = EgresoGenerales
		fields = ['folio_de_recibo','concepto','descripcion','monto','fecha',
			'pago_hecho_a','factura','proxima_fecha_de_pago','monto_futuro_a_cubrir',
			'realizo_pago']

class EgresoSuperUserForm(ModelForm):
	class Meta:
		model = EgresoGenerales
		fields = ['folio_de_recibo','concepto','descripcion','monto', 'fecha',
			'pago_hecho_a','factura','proxima_fecha_de_pago','monto_futuro_a_cubrir',
			'realizo_pago','movimiento_verificado_por_direccion', ]

class EgresoGeneralesAdmin(admin.ModelAdmin):
	search_fields = ('realizo_pago',)
	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser:
			kwargs['form'] = EgresoSuperUserForm
		else:
			kwargs['form'] = EgresoNormalUserForm
		return super(EgresoGeneralesAdmin, self).get_form(request, obj, **kwargs)
admin.site.register(EgresoGenerales,EgresoGeneralesAdmin)