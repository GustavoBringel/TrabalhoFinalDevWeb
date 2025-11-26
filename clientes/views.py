from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from django.db.models import Q

def listar_clientes(request):
    # Obtém todos os clientes inicialmente
    clientes = Cliente.objects.all().order_by('nome')
    
    # 1. Quantidade Cadastrada (Total)
    quantidade_total = clientes.count()
    
    # 2. Campo de Busca
    termo_busca = request.GET.get('q')
    
    if termo_busca:
        # Filtra pelo termo de busca no nome OU telefone OU email
        clientes = clientes.filter(
            Q(nome__icontains=termo_busca) |
            Q(telefone__icontains=termo_busca) |
            Q(email__icontains=termo_busca)
        )

    # 3. Quantidade exibida após o filtro
    quantidade_filtrada = clientes.count()

    context = {
        'clientes': clientes,
        'quantidade_total': quantidade_total,
        'quantidade_filtrada': quantidade_filtrada,
        'termo_busca': termo_busca, # Para manter o valor no campo de busca
    }
    return render(request, 'clientes/listar.html', context)

def cadastrar_editar_cliente(request, pk=None):
    if pk:
        # Se pk existe, estamos editando
        cliente = get_object_or_404(Cliente, pk=pk)
        titulo_acao = "Edição"
    else:
        # Se pk não existe, estamos cadastrando
        cliente = None
        titulo_acao = "Cadastro"

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            
            if pk:
                messages.success(request, f'Cliente {form.instance.nome} atualizado com sucesso!')
            else:
                messages.success(request, f'Cliente {form.instance.nome} cadastrado com sucesso!')
                
            return redirect('listar-clientes')
    else:
        # Método GET
        form = ClienteForm(instance=cliente)

    context = {
        'form': form,
        'cliente': cliente, # Passa o objeto cliente para o template (para o título de edição)
    }
    return render(request, 'clientes/novo.html', context)

def deletar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente {cliente.nome} excluído com sucesso.')
        return redirect('listar-clientes') # Redireciona para a lista
        
    context = {
        'cliente': cliente, # Variável usada no template
    }
    return render(request, 'clientes/confirm_delete.html', context)
