from __future__ import unicode_literals
from django.apps import AppConfig



class ControlEscolarConfig(AppConfig):
    name = 'controlescolar'
    def ready(self):
    	from controlescolar import signals
