# Seu arquivo forms.py
from django import forms
from .models import Servico # Você deve ter este modelo definido

class ServicoForm(forms.ModelForm):
    """
    Formulário para Cadastro e Edição de Serviços.
    """

    class Meta:
        model = Servico
        # Campos que aparecerão no formulário
        fields = ['nome', 'preco', 'duracao_minutos', 'descricao']
        
        labels = {
            'nome': 'Nome do Serviço',
            'preco': 'Preço (R$)',
            'duracao_minutos': 'Duração (em minutos)',
            'descricao': 'Detalhes ou Observações do Serviço',
        }
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Corte Feminino'}),
            # Usamos NumberInput com step para garantir valores decimais para o preço
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 60'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }