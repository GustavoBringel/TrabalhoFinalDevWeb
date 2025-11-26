from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from clientes.models import Cliente 
from servicos.models import Servico

class Agendamento(models.Model):
    """Gerencia um horário marcado para um cliente e serviço específico."""
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONFIRMADO', 'Confirmado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT, # Não permite apagar um cliente com agendamentos
        related_name='agendamentos'
    )
    servico = models.ForeignKey(
        Servico, 
        on_delete=models.PROTECT,
        related_name='agendamentos'
    )
    data_hora = models.DateTimeField(
        default=timezone.now,
        help_text="Data e hora de início do agendamento."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='AGENDADO'
    )
    notas = models.TextField(
        blank=True, 
        null=True,
        help_text="Qualquer nota específica sobre este agendamento."
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        # Garante que a agenda seja ordenada pela data mais próxima
        ordering = ['data_hora'] 
        
    def __str__(self):
        return f"Agenda: {self.cliente.nome} - {self.servico.nome} ({self.data_hora.strftime('%d/%m %H:%M')})"