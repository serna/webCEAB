import django_tables2 as tables
from promotoria.models import Aspirantes
from controlescolar.models import Estudiante
class AspiranteTable(tables.Table):
    class Meta:
        model = Aspirantes
        sequence = {'nombre',
        		'apellido_paterno',
        		'promotor',
        		'creacion_de_registro',
                'apellido_materno',
        		}
        fields = {'nombre',
                'apellido_paterno',
                'apellido_materno',
                'promotor',
                'creacion_de_registro',
                }
class EstudianteTable(tables.Table):
    class Meta:
        model = Estudiante
        sequence = {'fecha_de_registro',
                'plantel',
                'Aspirante',
                'numero_de_control',
                'creacion_de_registro',
                'empresa',
                'curso',
                'estatus',
                }
        fields = {'fecha_de_registro',
                'plantel',
                'Aspirante',
                'numero_de_control',
                'creacion_de_registro',
                'empresa',
                'curso',
                'estatus',
                }