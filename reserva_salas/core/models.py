from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class Sala(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.PositiveIntegerField()
    descricao = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} (Capacidade: {self.capacidade})"

class Reserva(models.Model):
    HORARIOS = [
        (8, '08:00 - 09:00'),
        (9, '09:00 - 10:00'),
        (10, '10:00 - 11:00'),
        (11, '11:00 - 12:00'),
        (12, '12:00 - 13:00'),
        (13, '13:00 - 14:00'),
        (14, '14:00 - 15:00'),
        (15, '15:00 - 16:00'),
        (16, '16:00 - 17:00'),
        (17, '17:00 - 18:00'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.IntegerField(choices=HORARIOS)
    criado_em = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('sala', 'data', 'horario')
        ordering = ['data', 'horario']

    def __str__(self):
        return f"{self.sala.nome} - {self.data} ({self.get_horario_display()}) por {self.usuario.username}"

    def clean(self):
        if self.data < datetime.date.today():
            raise ValidationError("Não é possível reservar para datas passadas.")
        
        if Reserva.objects.filter(sala=self.sala, data=self.data, horario=self.horario).exists():
            raise ValidationError("Esta sala já está reservada para este horário.")