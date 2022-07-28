from django.contrib import admin
from medicar.models import *
from medicar.forms import AgendaForm

class Medicos(admin.ModelAdmin):
    list_display = ('id','nome','crm','email')
    list_display_links = ('id','nome')

class HorariosInline(admin.TabularInline):
    model = Horarios
    list_display = ('agenda','horario',)

class Agendas(admin.ModelAdmin):
    form = AgendaForm
    list_display = ('medico','data_agenda')
    inlines = [
        HorariosInline,
    ]
    
admin.site.register(Agenda,Agendas)
admin.site.register(Medico,Medicos)   
#admin.site.register(Horarios,Horario)
