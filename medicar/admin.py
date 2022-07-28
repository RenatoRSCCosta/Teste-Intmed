from medicar.forms import AgendaForm, HorariosForm
from django.contrib import admin
from medicar.models import *


class Medicos(admin.ModelAdmin):
    list_display = ('id','nome','crm','email')
    list_display_links = ('id','nome')

class HorariosInline(admin.TabularInline):
    model = Horario
    form = HorariosForm

class Agendas(admin.ModelAdmin):
    form = AgendaForm
    list_display = ('medico','data_agenda')
    inlines = [
        HorariosInline,
    ]
    
admin.site.register(Agenda,Agendas)
admin.site.register(Medico,Medicos)
