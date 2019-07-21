from django.utils import timezone
from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from siad.models import Plantel, Horario, Empresa
from contabilidad.models import CorteCaja

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
class form_acceso_alumno(forms.Form):
	numero_de_alumno = forms.CharField(label = 'Ingresa tu numero de identificacion')
	clave_de_alumno = forms.CharField(label = 'Ingresa tu contrasena')
class form_busca_alumno_nombre(forms.Form):
	""" Este formulario busca a un alumno por su nombre"""
	nombre = forms.CharField(label='Nombre')
	apellido_paterno = forms.CharField(label='Apellido paterno',required=False)
	apellido_materno = forms.CharField(label='Apellido materno',required=False)
	
class rango_fechas_form(forms.Form):
	fecha_inicial = forms.DateField(widget=forms.SelectDateWidget())
	fecha_final = forms.DateField(widget=forms.SelectDateWidget())
class fecha_form(forms.Form):
	# se usa este formulario para consultas donde solo se necesita una fecha
	fecha = forms.DateField(widget=forms.SelectDateWidget(),initial=timezone.now)
class empresaFecha_form(forms.Form):
	# se usa este formulario para consultas donde solo se necesita una fecha
	empresa = forms.ModelChoiceField(queryset = Empresa.objects.all())
	fecha = forms.DateField(widget=forms.SelectDateWidget(),initial=timezone.now)

class fechaPlantel_form(forms.Form):
	# se usa este formulario para consultas donde solo se necesita una fecha
	plantel = forms.ModelChoiceField(queryset = Plantel.objects.all())
	fecha = forms.DateField(widget=forms.SelectDateWidget(),initial=timezone.now())


class form_captura_cal(forms.Form):
	# se usa este formulario para consultas donde solo se necesita una fecha
	alumno = forms.IntegerField()
	materia = forms.IntegerField()
	calificacion = forms.DecimalField(max_value = 10.0, min_value = 0.0, max_digits = 3)
class form_boleta_alumno(forms.Form):
	# se usa este formulario para consultas donde solo se necesita una fecha
	alumno = forms.IntegerField()
class form_plantel_empresa_horario(forms.Form):
	plantel = forms.ModelChoiceField(queryset = Plantel.objects.all())
	empresa = forms.ModelChoiceField(queryset = Empresa.objects.all())
	horario = forms.ModelChoiceField(queryset = Horario.objects.all())
class form_plantel(forms.Form):
	plantel = forms.ModelChoiceField(queryset = Plantel.objects.all())
class form_empresa(forms.Form):
	empresa = forms.ModelChoiceField(queryset = Empresa.objects.all())
class form_no_alumno(forms.Form):
	# se usa este formulario para consultas donde solo se necesita una fecha
	alumno = forms.IntegerField()
class form_genera_extraordinario(forms.Form):
	alumno = forms.IntegerField()
	materia = forms.IntegerField()
	
class form_corte_caja(ModelForm):
	class Meta:
		model = CorteCaja
		fields = ['folio','fecha_de_corte','ingresos','egresos','observaciones']
class preguntas_form(forms.Form):
	optionChoices = ((0,'a'), (1,'b'), (2,'c'),(3,'d'))
	#nombre = forms.CharField(widget=forms.TextInput())
	#clave_de_alumno = forms.CharField(widget=forms.NumberInput(attrs={'size': '4'}))
	numero_de_preguntas = forms.CharField(widget=forms.NumberInput(attrs={'size': '4'}))
	clave_del_examen = forms.CharField(widget=forms.NumberInput(attrs={'size': '4'}))
	#version_examen = forms.CharField(widget=forms.NumberInput(attrs={'size': '4'}))
	pregunta_1 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_2 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_3 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_4 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_5 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_6 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_7 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_8 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_9 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_10 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_11 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_12 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_13 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_14 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_15 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_16 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_17 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_18 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_19 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_20 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_21 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_22 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_23 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_24 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_25 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_26 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_27 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_28 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_29 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_30 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_31 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_32 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_33 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_34 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_35 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_36 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_37 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_38 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_39 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_40 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_41 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_42 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_43 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_44 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_45 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_46 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_47 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_48 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_49 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_50 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_51 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_52 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_53 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_54 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_55 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_56 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_57 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_58 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_59 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_60 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_61 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_62 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_63 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_64 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_65 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_66 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_67 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_68 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_69 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_70 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_71 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_72 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_73 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_74 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_75 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_76 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_77 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_78 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_79 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_80 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_81 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_82 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_83 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_84 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_85 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_86 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_87 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_88 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_89 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_90 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_91 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_92 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_93 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_94 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_95 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_96 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_97 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_98 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_99 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_100 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_101 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_102 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_103 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_104 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_105 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_106 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_107 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_108 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_109 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_110 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_111 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_112 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_113 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_114 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_115 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_116 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_117 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_118 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_119 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_120 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_121 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_122 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_123 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_124 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_125 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_126 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_127 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_128 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_129 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_130 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_131 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_132 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_133 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_134 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_135 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_136 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_137 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_138 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_139 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_140 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_141 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_142 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_143 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_144 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_145 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_146 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_147 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_148 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_149 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_150 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_151 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_152 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_153 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_154 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_155 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_156 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_157 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_158 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_159 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_160 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_161 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_162 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_163 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_164 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_165 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_166 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_167 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_168 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_169 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_170 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_171 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_172 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_173 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_174 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_175 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_176 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_177 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_178 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_179 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_180 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_181 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_182 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_183 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_184 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_185 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_186 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_187 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_188 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_189 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_190 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_191 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_192 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_193 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_194 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_195 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_196 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_197 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_198 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_199 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_200 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_201 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_202 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_203 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_204 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_205 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_206 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_207 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_208 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_209 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_210 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_211 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_212 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_213 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_214 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_215 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_216 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_217 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_218 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_219 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_220 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)
	pregunta_221 = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=optionChoices, required=False)