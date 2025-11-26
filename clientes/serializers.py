# clientes/serializers.py

from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Cliente."""
    class Meta:
        # Qual modelo estamos serializando
        model = Cliente
        # Quais campos do modelo devem ser incluídos na API
        # '__all__' inclui todos os campos. Você pode listar campos específicos se preferir.
        fields = '__all__'
        # Exemplo: fields = ['id', 'nome', 'telefone', 'email']