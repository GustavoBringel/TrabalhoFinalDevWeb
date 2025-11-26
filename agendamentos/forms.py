# agendamento/forms.py

from django import forms
from .models import Agendamento

# Importações dos modelos de outras apps (necessário se o Agendamento estiver separado)
from clientes.models import Cliente 
from servicos.models import Servico 

class AgendamentoForm(forms.ModelForm):
    """
    Formulário para criar ou editar um Agendamento.
    """
    
    # Adicionamos um widget personalizado para o campo data_hora
    # para usar recursos de calendário (se disponíveis no front-end)
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Data e Hora do Início'
    )
    
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'data_hora', 'status', 'notas']
        
        labels = {
            'cliente': 'Cliente',
            'servico': 'Serviço Agendado',
            'data_hora': 'Data e Hora',
            'status': 'Status do Agendamento',
            'notas': 'Notas do Agendamento',
        }
        
        widgets = {
            # O Select faz a lista drop-down de Clientes e Serviços
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'servico': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # Você pode adicionar validações de horário aqui (ex: checar conflitos)
    # def clean_data_hora(self):
    #     # ... Lógica de checagem de horário
    #     pass