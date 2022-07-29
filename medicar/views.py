from django.db.models import Q
from rest_framework.viewsets import mixins,GenericViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from medicar.serializer import *
from medicar.validators import *
from medicar.models import *

class ConsultasViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    """Gerencia os endpoints de consulta, metodos disponiveis (GET, POST, DELETE)"""
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        hoje = datetime.now().strftime('%Y-%m-%d')
        agora = datetime.now().strftime('%H:%M')

        return self.queryset.filter(Q(agenda__data_agenda__gt = hoje) 
                                  | Q(agenda__data_agenda = hoje, horario__horario__gte = agora)).order_by('agenda__data_agenda','horario__horario')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ConsultaSerializer(queryset, many = True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'agenda_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'horario': openapi.Schema(type=openapi.TYPE_STRING),
        }))

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
        if consulta is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if consulta.agenda.data_agenda <= today:
            raise APIException('não é possivel desmarcar uma consulta passada')

        horario = Horario.objects.get(pk = consulta.horario_id)
        horario.valido = True
        horario.save()
        consulta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                           
class AgendasViewSet(mixins.ListModelMixin,
                     GenericViewSet):
    """Gerencia os endpoints de agenda, metodos disponiveis (GET)"""
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

    medico = openapi.Parameter('medico', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING)
    crm = openapi.Parameter('crm', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING)
    data_inicio = openapi.Parameter('data_inicio', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING)
    data_final = openapi.Parameter('data_final', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(
        manual_parameters=[medico,crm,data_inicio,data_final],
    )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = AgendaSerializer(queryset, many = True)
        return Response(serializer.data)
        
