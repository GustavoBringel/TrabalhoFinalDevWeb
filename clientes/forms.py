from django import forms
from .models import Cliente # Importe o seu modelo de Cliente

class ClienteForm(forms.ModelForm):
    """
    Formulário baseado no modelo Cliente, usado para Cadastro e Edição.
    """
    
    # Você pode adicionar campos customizados aqui, se necessário.
    # Exemplo: um campo de confirmação de email que não está no modelo.
    # email_confirmacao = forms.EmailField(label='Confirme o Email')

    class Meta:
        model = Cliente
        # Defina quais campos do modelo Cliente serão exibidos no formulário.
        fields = ['nome', 'telefone', 'email', 'observacoes']
        
        # Opcional: Personalize os labels (nomes) dos campos
        labels = {
            'nome': 'Nome Completo do Cliente',
            'telefone': 'Telefone/WhatsApp',
            'email': 'Endereço de Email',
            'observacoes': 'Notas Importantes (Ex: Alergias, preferências)',
        }
        
        # Opcional: Adicione classes CSS do Bootstrap/CoreUI para estilização
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maria Silva'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (XX) 99999-9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex: maria.silva@exemplo.com'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }