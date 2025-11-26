# agendamentos/serializers.py

from rest_framework import serializers
from .models import Agendamento
from clientes.models import Cliente
from servicos.models import Servico

class AgendamentoSerializer(serializers.ModelSerializer):
    # Campos de chave estrangeira (FKs) para melhor visualização na API.

    # 1. Campo de Leitura (read_only=True): Exibe o nome do cliente.
    # Usado apenas para GET (leitura).
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    # 2. Campo de Escrita (para criação/edição): Permite enviar o ID do cliente.
    # Usa PK (Primary Key) do modelo Cliente para o campo 'cliente'.
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())

    # 3. Campo de Leitura: Exibe o nome do serviço.
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    
    # 4. Campo de Escrita: Permite enviar o ID do serviço.
    servico = serializers.PrimaryKeyRelatedField(queryset=Servico.objects.all())

    class Meta:
        model = Agendamento
        # Incluímos todos os campos do modelo, mais os campos auxiliares '_nome'
        fields = [
            'id', 
            'cliente', 
            'cliente_nome', # Apenas para visualização
            'servico', 
            'servico_nome', # Apenas para visualização
            'data_hora', 
            'status', 
            'notas', 
            'data_criacao'
        ]
        # Garantir que a data_hora é um campo required no POST/PUT
        extra_kwargs = {
            'data_hora': {'required': True}
        }