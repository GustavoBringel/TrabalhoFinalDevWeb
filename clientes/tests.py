# clientes/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from clientes.models import Cliente
from clientes.forms import ClienteForm

class ClienteViewTest(TestCase):
    """
    Testes para as views da aplicação clientes.
    """
    
    def setUp(self):
        """Configuração inicial para todos os testes."""
        self.client = Client()
        
        # URLs nomeadas (garanta que as URLS do projeto estão configuradas)
        self.url_listar = reverse('listar-clientes')
        self.url_cadastrar = reverse('cadastrar-cliente')
        
        # Criar clientes de teste para a listagem e busca
        self.cliente_1 = Cliente.objects.create(
            nome='Ana Silva', 
            telefone='9999-1111', 
            email='ana.silva@teste.com'
        )
        self.cliente_2 = Cliente.objects.create(
            nome='Bruno Souza', 
            telefone='9888-2222', 
            email='bruno.souza@corp.com'
        )
        self.cliente_3 = Cliente.objects.create(
            nome='Carlos Alberto', 
            telefone='9777-3333', 
            email='carlos@teste.com'
        )
        self.url_editar_1 = reverse('editar-cliente', args=[self.cliente_1.pk])
        self.url_deletar_1 = reverse('deletar-cliente', args=[self.cliente_1.pk])

# --- Testes de Listagem e Busca ---

    def test_1_listar_clientes_status_code(self):
        """Verifica se a view listar_clientes carrega corretamente."""
        response = self.client.get(self.url_listar)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientes/listar.html')

    def test_2_listar_clientes_contexto(self):
        """Verifica se o contexto da listagem está correto (quantidades)."""
        response = self.client.get(self.url_listar)
        self.assertEqual(response.context['quantidade_total'], 3)
        self.assertEqual(response.context['quantidade_filtrada'], 3)
        self.assertIn(self.cliente_1, response.context['clientes'])

    def test_3_listar_clientes_busca_por_nome(self):
        """Deve filtrar clientes por parte do nome."""
        response = self.client.get(self.url_listar + '?q=ana')
        self.assertEqual(response.context['quantidade_filtrada'], 1)
        self.assertIn(self.cliente_1, response.context['clientes'])
        self.assertNotIn(self.cliente_2, response.context['clientes'])
        self.assertContains(response, self.cliente_1.nome)

    def test_4_listar_clientes_busca_por_telefone(self):
        """Deve filtrar clientes pelo telefone."""
        response = self.client.get(self.url_listar + '?q=9888')
        self.assertEqual(response.context['quantidade_filtrada'], 1)
        self.assertIn(self.cliente_2, response.context['clientes'])

    def test_5_listar_clientes_busca_por_email(self):
        """Deve filtrar clientes por email (icontains)."""
        response = self.client.get(self.url_listar + '?q=corp.com')
        self.assertEqual(response.context['quantidade_filtrada'], 1)
        self.assertIn(self.cliente_2, response.context['clientes'])

# --- Testes de Cadastro (Novo Cliente) ---

    def test_6_cadastrar_cliente_get(self):
        """Verifica se a view de cadastro (GET) carrega o formulário corretamente."""
        response = self.client.get(self.url_cadastrar)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ClienteForm)
        self.assertTemplateUsed(response, 'clientes/novo.html')

    def test_7_cadastrar_cliente_post_sucesso(self):
        """Deve criar um novo cliente e redirecionar com mensagem de sucesso."""
        dados_novo = {
            'nome': 'Novo Cliente Teste',
            'telefone': '9666-4444',
            'email': 'novo@email.com',
        }
        
        response = self.client.post(self.url_cadastrar, dados_novo, follow=True)
        
        # Verifica redirecionamento e mensagem de sucesso
        self.assertRedirects(response, self.url_listar)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('cadastrado com sucesso!', str(messages[0]))
        
        # Verifica se o objeto foi criado no banco de dados
        self.assertEqual(Cliente.objects.count(), 4)
        novo_cliente = Cliente.objects.get(nome='Novo Cliente Teste')
        self.assertEqual(novo_cliente.email, 'novo@email.com')

    def test_8_cadastrar_cliente_post_invalido(self):
        """Não deve cadastrar cliente com dados inválidos (ex: nome vazio)."""
        dados_invalido = {
            'nome': '', # Inválido
            'telefone': '1234-5678',
            'email': 'invalido@email.com',
        }
        response = self.client.post(self.url_cadastrar, dados_invalido)
        
        # Deve retornar status 200 (re-renderiza o formulário)
        self.assertEqual(response.status_code, 200)
        # Verifica se o objeto NÃO foi criado
        self.assertEqual(Cliente.objects.count(), 3) 
        # Verifica se o formulário contém o erro (depende do seu template/validação)
        self.assertFormError(response.context['form'], 'nome', 'Este campo é obrigatório.')


# --- Testes de Edição ---

    def test_9_editar_cliente_get(self):
        """Verifica se a view de edição (GET) carrega o cliente correto."""
        response = self.client.get(self.url_editar_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana Silva') # Verifica se os dados do cliente 1 estão na página

    def test_10_editar_cliente_post_sucesso(self):
        """Deve atualizar o cliente existente e redirecionar com sucesso."""
        dados_edicao = {
            'nome': 'Ana Silva Atualizada', # Novo nome
            'telefone': '9999-1111', 
            'email': 'ana.silva.novo@teste.com', # Novo email
        }
        response = self.client.post(self.url_editar_1, dados_edicao, follow=True)
        
        # Verifica redirecionamento e mensagem de sucesso
        self.assertRedirects(response, self.url_listar)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('atualizado com sucesso!', str(messages[0]))
        
        # Verifica se o objeto foi atualizado no banco de dados
        cliente_atualizado = Cliente.objects.get(pk=self.cliente_1.pk)
        self.assertEqual(cliente_atualizado.nome, 'Ana Silva Atualizada')
        self.assertEqual(cliente_atualizado.email, 'ana.silva.novo@teste.com')

# --- Testes de Exclusão ---

    def test_11_deletar_cliente_get(self):
        """Verifica se a view de deleção (GET) carrega a confirmação."""
        response = self.client.get(self.url_deletar_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientes/confirm_delete.html')
        self.assertContains(response, f'Cliente: "{self.cliente_1.nome}"')

    def test_12_deletar_cliente_post_sucesso(self):
        """Deve excluir o cliente e redirecionar com mensagem de sucesso."""
        
        # Verifica a contagem antes
        self.assertEqual(Cliente.objects.count(), 3)
        
        response = self.client.post(self.url_deletar_1, follow=True)
        
        # Verifica redirecionamento e mensagem de sucesso
        self.assertRedirects(response, self.url_listar)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(f'Cliente {self.cliente_1.nome} excluído com sucesso.', str(messages[0]))
        
        # Verifica se o objeto foi removido
        self.assertEqual(Cliente.objects.count(), 2)
        with self.assertRaises(Cliente.DoesNotExist):
            Cliente.objects.get(pk=self.cliente_1.pk)