from dataclasses import field, fields
from django.http import QueryDict
from rest_framework import serializers
from medicar.models import Agenda, Medico, Horarios, Consultas
from datetime import date, datetime 
from medicar.validators import *

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class HorariosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Horarios
        fields = (
            'id',
            'horario',
        )
    def to_representation(self, instance):
        return str(instance.horario)[:5]

class AgendaSerializer(serializers.ModelSerializer):
    valid = valida_agenda()
    medico = MedicoSerializer(many = False, read_only = False)
    horarios = serializers.SerializerMethodField('get_horarios')

    def get_horarios(self, agenda):
        queryset = Horarios.objects.filter(agenda_id = agenda.id, valido = True)
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
    medico = serializers.SerializerMethodField('get_medico')
    horario = HorariosSerializer(many = False, read_only = False)
    dia = serializers.SerializerMethodField('get_dia')

    def get_medico(self, consulta):
        queryset = Medico.objects.get(pk = consulta.agenda.medico.id)
        return MedicoSerializer(instance = queryset).data

    def get_dia(self, consulta):
        queryset = Agenda.objects.get(pk = consulta.agenda.id)
        dia = queryset.data_agenda
        return dia

    class Meta:
        model = Consultas
        fields = (
            'id',
            'dia',
            'horario',
            'data_agendamento',
            'medico',
        )