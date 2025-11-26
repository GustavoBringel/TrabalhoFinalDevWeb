from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Servico
from .forms import ServicoForm
from .serializers import ServicoSerializer
from rest_framework import viewsets, permissions

# 1. VIEW DE LISTAGEM E BUSCA
def listar_servicos(request):
    servicos_qs = Servico.objects.all().order_by('nome')
    termo_busca = request.GET.get('q')

    if termo_busca:
        servicos_qs = servicos_qs.filter(
            Q(nome__icontains=termo_busca) |
            Q(descricao__icontains=termo_busca)
        )
    
    quantidade_total = Servico.objects.count()
    quantidade_filtrada = servicos_qs.count()

    context = {
        'servicos': servicos_qs,
        'quantidade_total': quantidade_total,
        'quantidade_filtrada': quantidade_filtrada,
        'termo_busca': termo_busca,
    }
    return render(request, 'servicos/listar.html', context)


# 2. VIEW DE CADASTRO/EDIÇÃO (Formulário Único)
def cadastrar_editar_servico(request, pk=None):
    if pk:
        # Modo Edição
        servico = get_object_or_404(Servico, pk=pk)
    else:
        # Modo Cadastro
        servico = None

    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            
            if pk:
                messages.success(request, f'Serviço "{form.instance.nome}" atualizado com sucesso!')
            else:
                messages.success(request, f'Serviço "{form.instance.nome}" cadastrado com sucesso!')
                
            return redirect('listar-servicos')
    else:
        # Método GET
        form = ServicoForm(instance=servico)

    context = {
        'form': form,
        'servico': servico,
    }
    return render(request, 'servicos/novo.html', context)


# 3. VIEW DE DELEÇÃO (Confirmação)
def deletar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)

    if request.method == 'POST':
        servico_nome = servico.nome
        servico.delete()
        messages.success(request, f'Serviço "{servico_nome}" excluído com sucesso.')
        return redirect('listar-servicos')

    context = {
        'servico': servico,
    }
    return render(request, 'servicos/confirm_delete.html', context)

class ServicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que serviços sejam vistos ou editados.
    """
    queryset = Servico.objects.all().order_by('nome')
    serializer_class = ServicoSerializer
    # Define as permissões (apenas usuários autenticados podem modificar)
    permission_classes = [permissions.IsAuthenticated]