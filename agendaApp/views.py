from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
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
    def get(self, request, *args, **kwargs):
        # Lógica de busca
        query = request.GET.get('busca', '')
        veiculos = Veiculo.objects.all()
        if query:
            veiculos = veiculos.filter(
                Q(modelo__icontains=query) |
                Q(marca__icontains=query)
            )
        return render(request, 'veiculos/listar.html', {'lista_veiculos': veiculos})
home = HomeView.as_view()