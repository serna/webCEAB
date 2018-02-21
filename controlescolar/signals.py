from django.db.models.signals import post_save, pre_save,m2m_changed
from django.dispatch import receiver
from .models import Estudiante, Documentacion, Curso



#@receiver(post_save, sender=Estudiante)
#def my_handler(sender, instance,created,**kwargs):
#	print "A INSTANCE OF Boleta AND Documentacion HAS BEEEN CREATED",created
#	Boleta.objects.create(alumno=instance)
#	Documentacion.objects.create(alumno=instance)

#def materias_cambiaron(sender, instance,**kwargs):
    # Do something
	#instance = kwargs.pop('instance', None)
#	pk_set = kwargs.pop('pk_set', None)
	#print("LAS LLAVES ARGUMENTO SON: " + str(instance) + str(instance.materias.all()))
	#print(lista_materias)
	#if len(instance.boleta) == 0: # just do it the first time the instance is created
		#global lista_materias
		#lista_materias = ''
		#for item in instance.materias.all():
			#item = str(item).split(':')[0]
			#lista_materias += str(item)
			#lista_materias += '\n'
		#print(lista_materias)
		#instance.boleta = lista_materias
		#instance.save()
#m2m_changed.connect(materias_cambiaron, sender=Curso.materias.through)



#@receiver(pre_save, sender=Curso)
#def my_handler(sender,instance,**kwargs):
#	#if not(instance.id):
#	print("ESTO ES ANTES DE TODO " + str(lista_materias))
#	instance.boleta = lista_materias




#@receiver(m2m_changed, sender=Curso)
#def my_handler(sender, **kwargs):
#	instance = kwargs.pop('instance', None)
#	pk_set = kwargs.pop('pk_set', None)
#	print("LAS LLAVES ARGUMENTO SON: " + str(pk_set))   
#	if action == "pre_add":
#		for item in pk_set:
#			cadena += str(item) + "\n"
#		instance.boleta = cadena

#@receiver(m2m_changed, sender=Curso)
#def my_handler(sender,instance,**kwargs):
#	if instance.id:
#		if len(instance.boleta)== 0:
#			print ("The fields of materias has been created: " + str(instance.materias))
#			
#	else:
#		instance.save()