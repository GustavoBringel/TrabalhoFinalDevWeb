from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from agendamentos.models import Agendamento
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class HomeView(LoginRequiredMixin, View):
    # O nome do método deve ser 'get' para lidar com requisições HTTP GET
    def get(self, request):
        
        hoje = timezone.now().date() 

        # --- Lógica de Busca ---
        termo_busca = request.GET.get('q')

        # 1. Agendamentos de Hoje
        agendamentos_hoje = Agendamento.objects.filter(
            data_hora__date=hoje
        ).order_by('data_hora')
        
        # 2. Agendamentos Futuros (excluindo hoje)
        agendamentos_futuros = Agendamento.objects.filter(
            data_hora__gt=timezone.now().replace(hour=23, minute=59, second=59)
        ).order_by('data_hora')

        # Aplicar filtro de busca se houver
        if termo_busca:
            filtro = Q(cliente__nome__icontains=termo_busca) | Q(servico__nome__icontains=termo_busca)
            agendamentos_hoje = agendamentos_hoje.filter(filtro)
            agendamentos_futuros = agendamentos_futuros.filter(filtro)

        # --- Contagens ---
        total_hoje = agendamentos_hoje.count()
        total_pendente = agendamentos_hoje.filter(status='AGENDADO').count()
        
        # --- Contexto e Renderização ---
        context = {
            'agendamentos_hoje': agendamentos_hoje,
            'agendamentos_futuros': agendamentos_futuros, 
            'total_hoje': total_hoje,
            'total_pendente': total_pendente,
            'termo_busca': termo_busca,
            'hoje': hoje,
        }
        
        return render(request, 'main.html', context)
    
home = HomeView.as_view()