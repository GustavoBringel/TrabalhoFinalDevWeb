# agendamento/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Agendamento
from .forms import AgendamentoForm
from django.utils import timezone # Para lidar com a data/hora

# -------------------------------------------------------------
# VIEW DE CADASTRO/EDIÇÃO (Novo Agendamento)
# -------------------------------------------------------------
def novo_editar_agendamento(request, pk=None):
    if pk:
        agendamento = get_object_or_404(Agendamento, pk=pk)
    else:
        agendamento = None

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            
            if pk:
                messages.success(request, 'Agendamento atualizado com sucesso!')
            else:
                messages.success(request, 'Novo agendamento criado com sucesso!')
                
            return redirect('listar-agendamentos') # Redireciona para a agenda
    else:
        # Método GET
        # Se for edição, ajusta o formato da data para o widget HTML5
        if agendamento and agendamento.data_hora:
            agendamento.data_hora = agendamento.data_hora.strftime('%Y-%m-%dT%H:%M')
            
        form = AgendamentoForm(instance=agendamento)

    context = {
        'form': form,
        'agendamento': agendamento,
    }
    return render(request, 'form_agendamento.html', context)


# -------------------------------------------------------------
# VIEW DE LISTAGEM/AGENDA (Tela Inicial)
# -------------------------------------------------------------
def listar_agendamentos(request):
    # Filtro padrão: agendamentos a partir de hoje
    agendamentos = Agendamento.objects.filter(
        data_hora__gte=timezone.now().date()
    ).order_by('data_hora')
    
    # Campo de Busca (Filtra por Cliente ou Serviço)
    termo_busca = request.GET.get('q')
    if termo_busca:
        agendamentos = agendamentos.filter(
            Q(cliente__nome__icontains=termo_busca) |
            Q(servico__nome__icontains=termo_busca)
        )

    # Contagens para o resumo na tela
    total_hoje = Agendamento.objects.filter(data_hora__date=timezone.now().date()).count()
    total_pendente = agendamentos.filter(status='AGENDADO').count()

    context = {
        'agendamentos': agendamentos,
        'total_hoje': total_hoje,
        'total_pendente': total_pendente,
        'termo_busca': termo_busca,
    }
    return render(request, 'listar_agendamentos.html', context)
    
# -------------------------------------------------------------
# VIEW DE DELEÇÃO (Para completar o CRUD)
# -------------------------------------------------------------
def deletar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    if request.method == 'POST':
        cliente_nome = agendamento.cliente.nome
        agendamento.delete()
        messages.success(request, f'Agendamento do cliente {cliente_nome} excluído com sucesso.')
        return redirect('listar-agendamentos')

    context = {
        'agendamento': agendamento,
    }
    return render(request, 'deletar_agendamento.html', context)