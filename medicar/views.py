from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from medicar.serializer import *
from medicar.validators import *
from django.db.models import Q
from medicar.models import *


class ConsultasViewSet(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    allowed_methods = ('GET','POST','DELETE')

    def get_queryset(self):
        hoje = datetime.now().strftime('%Y-%m-%d')
        agora = datetime.now().strftime('%H:%M')

        return self.queryset.filter(Q(agenda__data_agenda__gt = hoje) 
        | Q(agenda__data_agenda = hoje, horario__horario__gte = agora)).order_by('agenda__data_agenda','horario__horario')

    def create(self, request, *args, **kwargs):
        # Realiza a validação da agenda e dos horarios
        valid = valida_agenda()

        dados = request.data
        agenda = Agenda.objects.get(pk = dados['agenda_id'])
        horario = Horario.objects.get(horario = dados['horario'],agenda = dados['agenda_id'])       
        data_agendamento = datetime.now().strftime('%Y-%m-%d')

        if not horario.valido:
            raise APIException('Horario não disponivel para agendamento')
        if not agenda.valido:
            raise APIException('Agenda não disponivel para agendamento')

        nova_consulta = Consulta.objects.create(data_agendamento=data_agendamento, horario_id=horario.id, agenda_id=agenda.id)
        nova_consulta.save()
        horario.valido = False
        horario.save()
        serializer = ConsultaSerializer(nova_consulta)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        today = datetime.date(datetime.now())
        consulta = Consulta.objects.filter(pk=self.kwargs.get('pk')).first()
        print(consulta)
        print(today)
        if consulta is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if consulta.agenda.data_agenda <= today:
            raise APIException('não é possivel desmarcar uma consulta passada')

        horario = Horario.objects.get(pk = consulta.horario_id)
        horario.valido = True
        horario.save()
        consulta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgendasViewSet(ReadOnlyModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    
    def get_queryset(self):
        # Realiza a validação da agenda e dos horarios
        valid = valida_agenda()
        queryset = self.queryset
        hoje = datetime.now()
        medicos = self.request.query_params.getlist('medico')
        data_inicio = self.request.query_params.get('data_inicio')
        data_final = self.request.query_params.get('data_final')
        crm = self.request.query_params.getlist('crm')

        if medicos:
            queryset = queryset.filter(medico__id__in = medicos, valido = True, horarios__valido = True).order_by('data_agenda').distinct()
        if data_inicio and data_final:
            queryset = queryset.filter(data_agenda__range=(data_inicio, data_final),valido = True, horarios__valido = True).order_by('data_agenda').distinct()
        if crm:
            queryset = queryset.filter(medico__crm__in = crm, valido = True, horarios__valido = True).order_by('data_agenda').distinct()
        if not medicos and not data_inicio and not data_final and not crm:
            queryset = queryset.filter(data_agenda__gte=hoje.strftime('%Y-%m-%d'), valido = True, horarios__valido = True).order_by('data_agenda').distinct()

        return queryset
        
