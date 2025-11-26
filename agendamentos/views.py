from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone 
from datetime import timedelta # <-- NOVO IMPORT
from .models import Agendamento
from .forms import AgendamentoForm

# -------------------------------------------------------------
# VIEW DE CADASTRO/EDIÇÃO (Com Validações de Tempo e Conflito)
# -------------------------------------------------------------
def novo_editar_agendamento(request, pk=None):
    # (Restante da lógica inicial... obtendo agendamento ou None)
    if pk:
        agendamento = get_object_or_404(Agendamento, pk=pk)
    else:
        agendamento = None

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        
        if form.is_valid():
            
            # --- NOVO BLOCO DE LÓGICA: BYPASS ---
            
            # Checa se é EDIÇÃO e se APENAS o STATUS ou NOTAS foi alterado.
            data_hora_mudou = 'data_hora' in form.changed_data
            
            if agendamento and not data_hora_mudou:
                # Se for edição e a data/hora não mudou, salva e finaliza SEM checar tempo/conflito.
                form.save()
                messages.success(request, 'Status do agendamento atualizado com sucesso!')
                return redirect('listar-agendamentos')
            
            # --- FIM DO BLOCO DE BYPASS. As validações abaixo só rodam se for NOVO cadastro OU a DATA/HORA MUDOU. ---

            
            # Validações de Tempo e Conflito (APENAS se for NOVO ou DATA/HORA alterada)
            novo_agendamento_temp = form.save(commit=False)
            
            data_hora_agendamento = novo_agendamento_temp.data_hora
            servico = novo_agendamento_temp.servico 
            
            # ... (Restante do código de cálculo de tempo e duração) ...
            agora = timezone.now()
            tempo_minimo = agora + timedelta(minutes=30)
            
            duracao = timedelta(minutes=servico.duracao_minutos)
            data_hora_fim_novo = data_hora_agendamento + duracao
            
            # --- VALIDAÇÕES DE TEMPO E CONFLITO (SEMPRE APLICADAS QUANDO HÁ MUDANÇA DE HORÁRIO) ---
            
            # A. Validação 1: Não pode agendar no passado
            if data_hora_agendamento < agora:
                messages.error(request, 'Erro: Não é possível agendar em um horário que já passou.')
                return render(request, 'agendamentos/novo.html', {'form': form, 'agendamento': agendamento})

            # B. Validação 2: Mínimo de 30 minutos de antecedência
            if data_hora_agendamento < tempo_minimo:
                messages.error(request, f'Erro: Agendamentos devem ter no mínimo 30 minutos de antecedência. Tente após as {tempo_minimo.strftime("%H:%M")}.')
                return render(request, 'agendamentos/novo.html', {'form': form, 'agendamento': agendamento})
            
            # C. Validação 3: Conflito de Horário (A lógica de iteração continua aqui)
            
            conflitos_qs = Agendamento.objects.filter(
                data_hora__date=data_hora_agendamento.date()
            ).exclude(status='CANCELADO')

            if agendamento:
                conflitos_qs = conflitos_qs.exclude(pk=agendamento.pk)

            conflito_encontrado = False
            for existente in conflitos_qs:
                duracao_existente = timedelta(minutes=existente.servico.duracao_minutos)
                data_hora_fim_existente = existente.data_hora + duracao_existente
                
                if (existente.data_hora < data_hora_fim_novo) and (data_hora_agendamento < data_hora_fim_existente):
                    conflito_encontrado = True
                    break

            if conflito_encontrado:
                messages.error(request, f'Conflito de horários! O agendamento {existente.cliente.nome} ({existente.servico.nome}) ocupa este tempo.')
                return render(request, 'agendamentos/novo.html', {'form': form, 'agendamento': agendamento})

            # --- SALVAR (Se passar em todas as validações) ---
            novo_agendamento_temp.save() 
            
            # As mensagens de sucesso antigas continuam aqui
            if pk:
                messages.success(request, 'Agendamento atualizado com sucesso!')
            else:
                messages.success(request, 'Novo agendamento criado com sucesso!')
                
            return redirect('listar-agendamentos')
            
    else:
        # (Restante do método GET...)
        if agendamento and agendamento.data_hora:
            agendamento.data_hora = agendamento.data_hora.strftime('%Y-%m-%dT%H:%M')
            
        form = AgendamentoForm(instance=agendamento)

    context = {
        'form': form,
        'agendamento': agendamento,
    }
    return render(request, 'agendamentos/novo.html', context)


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
    return render(request, 'agendamentos/listar.html', context)
    
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
    return render(request, 'agendamentos/confirm_delete.html', context)