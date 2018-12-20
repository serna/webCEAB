"""webCEAB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index_original),
    url(r'^consultas$', views.consultas),
    url(r'^registroInexistente$', views.registro_inexistente),
    url(r'^alumnos$', views.accesoAlumno),
    url(r'^promotores$', views.menu_promotor),
    url(r'^prospectos_promotor$', views.prospectos_promotor),
    url(r'^inscritos_promotor$', views.inscritos_promotor),
    url(r'^cobros_diarios$', views.cobros_diarios),
    url(r'^pagos_proximos$', views.pagos_proximos),
    url(r'^genera_pdf$', views.genera_pdf),

    url(r'^cobros_vencidos/(?P<dias>\d+)$', views.cobros_vencidos),
    url(r'^eval/(?P<alumno>\d+)/(?P<materia>\d+)$', views.evaluacion_digital),
    url(r'^resumen_prospectos$', views.resumen_prospectos),
    url(r'^alumnos_con_servicio$', views.reporte_con_servicio),
    url(r'^inscritos_y_prospectos_por_fechas_de/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/a/(?P<year2>[0-9]{4})/(?P<month2>[0-9]{2})/(?P<day2>[0-9]{2})/$',views.reporte_inscritos_prospectos_por_fechas),
    url(r'^captura_calificacion$', views.captura_calificacion),
    url(r'^boleta_alumno$', views.boleta_alumno),
    url(r'^imprime_material_regulares$', views.imprime_material_regulares),
    url(r'^imprime_material_empresa$', views.imprime_material_empresa),
    url(r'^calendario_materias$', views.calendario_materias),
    url(r'^documentacion_incompleta_plantel$', views.documentacion_incompleta_plantel),
    url(r'^documentacion_incompleta_empresa$', views.documentacion_incompleta_empresa),
    url(r'^ingresos_del_dia$', views.ingresos_del_dia),
    url(r'^genera_extraordinario$', views.genera_extraordinario),
    url(r'^buscar_alumno_nombre$', views.buscar_alumno_nombre),
    url(r'^consulta_pagos_alumno$', views.consulta_pagos_alumno),
    url(r'^corte_caja$', views.corte_caja),
    url(r'^cobros_por_vencer$', views.cobros_por_vencer),

]
