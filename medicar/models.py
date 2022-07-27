from datetime import timedelta
from django.db import models

class Medico(models.Model):
    nome = models.CharField(max_length=50, blank=False)
    crm = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(blank=True, null = True)

    def __str__(self):
        return self.nome

class Agenda(models.Model):
    medico = models.ForeignKey(Medico,related_name="medico", on_delete = models.CASCADE)
    data_agenda = models.DateField()
    valido = models.BooleanField(default=True)

    def __str__(self):
        return f"Agenda de {self.medico.nome}: {self.data_agenda}"

    def horarios_validos(self):
        horarios_validos = self.horarios.filter(valido = True)
        return len(horarios_validos) > 0

    def invalidar(self):
        self.valido = False
        self.save()
        self.horarios.update(valido=False)
    
    class Meta:
        ordering = ['data_agenda']
    
class Horarios(models.Model):
    agenda = models.ForeignKey(Agenda, related_name="horarios", on_delete=models.CASCADE)
    horario = models.TimeField()
    status = models.CharField(max_length=2, default ='AG')
    valido = models.BooleanField(default=True)

    def __str___(self):
        return f"{self.horario}"
    
    def horarios_disponiveis(self):
        return self.filter(validado = True)

    class Meta:
        ordering = ['horario']
        unique_together = ('horario', 'agenda', )

class Consultas(models.Model):
    agenda = models.ForeignKey(Agenda, related_name="agenda", on_delete=models.CASCADE)
    horario = models.ForeignKey(Horarios, related_name="horarios", on_delete=models.CASCADE)
    data_agendamento = models.DateField(null = True)

    class Meta:
        ordering = ['data_agendamento']