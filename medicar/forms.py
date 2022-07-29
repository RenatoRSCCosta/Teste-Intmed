from medicar.validators import *
from medicar.models import *
from django import forms


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        exclude = ('valido',)

    def clean(self):
        data_agenda = self.cleaned_data.get('data_agenda')
        medico = self.cleaned_data.get('medico')
        lista_de_erros = {}
        if hasattr(self, 'instance') and self.instance.pk is not None:
            agenda_retroativa(data_agenda, lista_de_erros)
        else:        
            medico_com_agenda(medico, data_agenda, lista_de_erros)
            agenda_retroativa(data_agenda, lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class HorariosForm(forms.ModelForm):
    class Meta:
        model = Horario
        exclude = ('valido',)

    def clean(self):
        horario = self.cleaned_data.get('id')
        lista_de_erros = {}
        if horario:
            horario_pode_editar(horario.id, lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

