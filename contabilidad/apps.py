from django.apps import AppConfig


class ContabilidadConfig(AppConfig):
    name = 'contabilidad'
    def ready(self):
    	from contabilidad import signals
