from datetime import date, datetime 
from medicar.models import Agenda, Horarios

def agenda_retroativa(data_agenda, lista_de_erros):
    """Verifica se a agenda está sendo criada para um dia retroativo"""
    today = datetime.date(datetime.now())
    if data_agenda < today:
        lista_de_erros['data_agenda'] = "Não é possivel criar agenda em dias retroativos"

def medico_com_agenda(medico, data_agenda, lista_de_erros):
    """Verifica se o medico já possui uma agenda na mesma data"""
    agenda = Agenda.objects.filter(medico = medico, data_agenda = data_agenda)
    if agenda:
        lista_de_erros['medico'] = "Não é possivel criar mais de uma agenda para o mesmo medico no mesmo dia"


def valida_agenda():
    """Realiza validações de datas e horarios passados"""
    #invalida agendas que a data já passou
    datas_passadas = Agenda.objects.filter(data_agenda__lt=date.today())
    for data_passada in datas_passadas:
        data_passada.invalidar()
    #invalidar horarios de hoje que já passou da hora atual
    horas_passadas = Horarios.objects.filter(agenda__data_agenda = date.today(), horario__lt = datetime.now().time())
    horas_passadas.update(valido = False)
    #invalidar agendas que todos os horarios estao invalidos
    agendas_validas = Agenda.objects.filter(valido = True)
     
    for agenda in agendas_validas:
        if not agenda.horarios_validos():
            agenda.invalidar()
