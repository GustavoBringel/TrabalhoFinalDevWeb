from django.db import models

class Cliente(models.Model):
    """Representa o cliente que agenda o serviço."""
    nome = models.CharField(max_length=150)
    telefone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Número para contato, idealmente com WhatsApp."
    )
    email = models.EmailField(
        max_length=100, 
        blank=True, 
        null=True
    )
    observacoes = models.TextField(
        blank=True, 
        null=True,
        help_text="Notas importantes, como alergias ou preferências."
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome
