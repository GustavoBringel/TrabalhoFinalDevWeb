# servicos/serializers.py

from rest_framework import serializers
from .models import Servico

class ServicoSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Servico."""
    class Meta:
        model = Servico
        # Inclui todos os campos: id, nome, duracao_minutos, preco
        fields = '__all__'