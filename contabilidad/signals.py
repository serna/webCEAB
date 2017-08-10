from django.db.models.signals import post_save, pre_save,m2m_changed
from django.dispatch import receiver
from .models import PagosAlumno
from controlescolar.models import Curso

@receiver(pre_save, sender=PagosAlumno)
def my_handler(sender,instance,**kwargs):
	if not(instance.id):
		print(instance.monto)
		print(instance.curso_a_pagar)
		print(instance.curso_a_pagar.id)
		try:
			obj = Curso.objects.get(id=instance.curso_a_pagar.id)
			obj.adeudo -= instance.monto
			obj.save()
		except Curso.DoesNotExist:
			print("No se pudo realizar la operacion de actualizar el monto")
		print(obj)