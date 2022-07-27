from django.contrib import admin
from medicar.models import *
from medicar.forms import AgendaForm

class Medicos(admin.ModelAdmin):
    list_display = ('id','nome','crm','email')
    list_display_links = ('id','nome')

class Agendas(admin.ModelAdmin):
    form = AgendaForm
    list_display = ('medico','data_agenda')

class Horario(admin.ModelAdmin):
    list_display = ('agenda','horario',)
    
admin.site.register(Agenda,Agendas)
admin.site.register(Medico,Medicos)   
admin.site.register(Horarios,Horario)
