from django.db import models
from django.core.validators import MinValueValidator


class Servico(models.Model):
    """Representa um serviço oferecido pelo salão."""
    nome = models.CharField(max_length=150)
    preco = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    duracao_minutos = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duração estimada do serviço em minutos."
    )
    descricao = models.TextField(
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"
