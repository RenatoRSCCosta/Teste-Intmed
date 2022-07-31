from cProfile import label
from rest_framework import serializers
from medicar.validators import *
from medicar.models import *

class MedicoSerializer(serializers.ModelSerializer):
    """Serializador do model de medico"""
    class Meta:
        model = Medico
        fields = '__all__'


class HorariosSerializer(serializers.ModelSerializer):
    """Serializador do model de horario"""
    class Meta:
        model = Horario
        fields = (
            'horario',
        )
    def to_representation(self, instance):
        return str(instance.horario)[:5]

class AgendaSerializer(serializers.ModelSerializer):
    """Serializador do model de agenda"""
    medico = MedicoSerializer(many = False, read_only = False)
    horarios = serializers.SerializerMethodField('get_horarios')

    # Retorna apenas horarios validos
    def get_horarios(self, agenda):
        queryset = Horario.objects.filter(agenda_id = agenda.id, valido = True)
        serializer = HorariosSerializer(instance = queryset, many = True)
        return serializer.data

    class Meta:
        model = Agenda
        fields = (
            'id',
            'medico',
            'data_agenda',
            'horarios'
        )

class ConsultaSerializer(serializers.ModelSerializer):
    """Serializador do model de consulta"""
    data_agendamento = serializers.DateField(read_only = True)
    agenda_id = serializers.IntegerField(read_only = False)
    horario = serializers.CharField(read_only = False)
    medico = serializers.SerializerMethodField('get_medico')
    dia = serializers.SerializerMethodField('get_dia')

    # Retorna os dados do medico
    def get_medico(self, consulta):
        queryset = Medico.objects.get(pk = consulta.agenda.medico.id)
        return MedicoSerializer(instance = queryset).data

    # Retorna o dia da agenda
    def get_dia(self, consulta):
        queryset = Agenda.objects.get(pk = consulta.agenda.id)
        dia = queryset.data_agenda
        return dia

    class Meta:
        model = Consulta
        fields = (
            'id',
            'dia',
            'agenda_id',
            'horario',
            'data_agendamento',
            'medico',
        )