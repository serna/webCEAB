from django.contrib import admin
from .models import Plantel, Empleado, ContactoEmpresarial, Empresa, FormaContacto, Documento, Estatus, FormaDePago, Horario,Calendario

class ContactoEmpresarialAdmin(admin.ModelAdmin):
	search_fields = ('nombre',)
admin.site.register(ContactoEmpresarial,ContactoEmpresarialAdmin)
admin.site.register(Plantel)
admin.site.register(Empleado)

admin.site.register(Empresa)
admin.site.register(FormaContacto)
admin.site.register(Documento)
admin.site.register(Estatus)
admin.site.register(FormaDePago)
admin.site.register(Horario)
admin.site.register(Calendario)
