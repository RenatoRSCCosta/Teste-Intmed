from django import forms
from medicar.models import Agenda
from medicar.validators import *

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('medico','data_agenda')

    def clean(self):
        data_agenda = self.cleaned_data.get('data_agenda')
        medico = self.cleaned_data.get('medico')
        lista_de_erros = {}
        agenda_retroativa(data_agenda, lista_de_erros)
        medico_com_agenda(medico, data_agenda, lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data