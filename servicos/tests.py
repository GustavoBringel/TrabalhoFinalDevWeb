# servicos/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from servicos.models import Servico
from servicos.forms import ServicoForm

class ServicoViewTest(TestCase):
    """
    Testes para as views da aplicação servicos (CRUD e Busca).
    """
    
    def setUp(self):
        """Configuração inicial: cliente de teste e objetos Servico."""
        self.client = Client()
        
        # URLs nomeadas (garanta que estão configuradas no urls.py)
        self.url_listar = reverse('listar-servicos')
        self.url_cadastrar = reverse('cadastrar-servico')
        
        # 1. Criar serviços de teste
        self.servico_1 = Servico.objects.create(
            nome='Corte Masculino', 
            preco=50.00, 
            duracao_minutos=45, 
            descricao='Corte clássico e moderno.'
        )
        self.servico_2 = Servico.objects.create(
            nome='Barba Clássica', 
            preco=35.00, 
            duracao_minutos=30, 
            descricao='Barba feita com toalha quente e finalização.'
        )
        self.servico_3 = Servico.objects.create(
            nome='Tintura de Cabelo', 
            preco=120.00, 
            duracao_minutos=90, 
            descricao='Aplicação de tintura permanente.'
        )

        self.url_editar_1 = reverse('editar-servico', args=[self.servico_1.pk])
        self.url_deletar_1 = reverse('deletar-servico', args=[self.servico_1.pk])

# ----------------------------------------------------------------------
# Testes de Listagem e Busca
# ----------------------------------------------------------------------

    def test_1_listar_servicos_status_code(self):
        """Verifica se a view listar_servicos carrega corretamente."""
        response = self.client.get(self.url_listar)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/listar.html')

    def test_2_listar_servicos_contexto_e_total(self):
        """Verifica se o contexto da listagem está correto (quantidades)."""
        response = self.client.get(self.url_listar)
        self.assertEqual(response.context['quantidade_total'], 3)
        self.assertEqual(response.context['quantidade_filtrada'], 3)
        self.assertIn(self.servico_1, response.context['servicos'])
        self.assertIn(self.servico_2.nome, response.content.decode())

    def test_3_listar_servicos_busca_por_nome(self):
        """Deve filtrar serviços por parte do nome (Corte)."""
        response = self.client.get(self.url_listar + '?q=corte')
        self.assertEqual(response.context['quantidade_filtrada'], 1)
        self.assertIn(self.servico_1, response.context['servicos'])
        self.assertNotIn(self.servico_2, response.context['servicos'])
        self.assertContains(response, self.servico_1.nome)

    def test_4_listar_servicos_busca_por_descricao(self):
        """Deve filtrar serviços por parte da descrição (toalha)."""
        response = self.client.get(self.url_listar + '?q=toalha')
        self.assertEqual(response.context['quantidade_filtrada'], 1)
        self.assertIn(self.servico_2, response.context['servicos'])
        self.assertContains(response, self.servico_2.nome)
        
    def test_5_listar_servicos_busca_vazia(self):
        """Busca por termo inexistente deve retornar zero resultados."""
        response = self.client.get(self.url_listar + '?q=inexistente')
        self.assertEqual(response.context['quantidade_filtrada'], 0)
        self.assertContains(response, "não retornou resultados.") # Assumindo que seu template mostra esta mensagem
        
# ----------------------------------------------------------------------
# Testes de Cadastro (Novo Serviço)
# ----------------------------------------------------------------------

    def test_6_cadastrar_servico_get(self):
        """Verifica se a view de cadastro (GET) carrega o formulário corretamente."""
        response = self.client.get(self.url_cadastrar)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ServicoForm)
        self.assertTemplateUsed(response, 'servicos/novo.html')

    def test_7_cadastrar_servico_post_sucesso(self):
        """Deve criar um novo serviço e redirecionar com mensagem de sucesso."""
        dados_novo = {
            'nome': 'Massagem Terapêutica',
            'preco': 80.00,
            'duracao_minutos': 60,
            'descricao': 'Massagem relaxante.',
        }
        
        response = self.client.post(self.url_cadastrar, dados_novo, follow=True)
        
        # Verifica redirecionamento e mensagem de sucesso
        self.assertRedirects(response, self.url_listar)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('cadastrado com sucesso!', str(messages[0]))
        
        # Verifica se o objeto foi criado no banco de dados
        self.assertEqual(Servico.objects.count(), 4)
        novo_servico = Servico.objects.get(nome='Massagem Terapêutica')
        self.assertEqual(novo_servico.duracao_minutos, 60)

    def test_8_cadastrar_servico_post_invalido(self):
        """Não deve cadastrar serviço com dados inválidos (ex: nome vazio)."""
        dados_invalido = {
            'nome': '', # Inválido
            'preco': 10.00,
            'duracao_minutos': 15,
            'descricao': 'Teste inválido',
        }
        response = self.client.post(self.url_cadastrar, dados_invalido)
        
        # Deve retornar status 200 (re-renderiza o formulário)
        self.assertEqual(response.status_code, 200)
        # Verifica se o objeto NÃO foi criado
        self.assertEqual(Servico.objects.count(), 3) 
        # Usa a string de erro em Inglês/Padrão (para robustez no ambiente de teste)
        self.assertFormError(response.context['form'], 'nome', 'Este campo é obrigatório.')


# ----------------------------------------------------------------------
# Testes de Edição
# ----------------------------------------------------------------------

    def test_9_editar_servico_get(self):
        """Verifica se a view de edição (GET) carrega o serviço correto."""
        response = self.client.get(self.url_editar_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Corte Masculino') 
        self.assertContains(response, self.servico_1.descricao)

    def test_10_editar_servico_post_sucesso(self):
        """Deve atualizar o serviço existente e redirecionar com sucesso."""
        dados_edicao = {
            'nome': 'Corte Masculino Premium', # Novo nome
            'preco': 60.00, 
            'duracao_minutos': 60, # Nova duração
            'descricao': self.servico_1.descricao,
        }
        response = self.client.post(self.url_editar_1, dados_edicao, follow=True)
        
        # Verifica redirecionamento e mensagem de sucesso
        self.assertRedirects(response, self.url_listar)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('atualizado com sucesso!', str(messages[0]))
        
        # Verifica se o objeto foi atualizado no banco de dados
        servico_atualizado = Servico.objects.get(pk=self.servico_1.pk)
        self.assertEqual(servico_atualizado.nome, 'Corte Masculino Premium')
        self.assertEqual(servico_atualizado.preco, 60.00)
        self.assertEqual(servico_atualizado.duracao_minutos, 60)

# ----------------------------------------------------------------------
# Testes de Exclusão
# ----------------------------------------------------------------------

    def test_11_deletar_servico_get(self):
        """Verifica se a view de deleção (GET) carrega a confirmação."""
        response = self.client.get(self.url_deletar_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicos/confirm_delete.html')
        
        # Assumindo que o template exibe o nome do serviço para confirmação
        self.assertContains(response, f'Serviço: "{self.servico_1.nome}"') 

    def test_12_deletar_servico_post_sucesso(self):
        """Deve excluir o serviço e redirecionar com mensagem de sucesso."""
        
        # Verifica a contagem antes
        self.assertEqual(Servico.objects.count(), 3)
        
        response = self.client.post(self.url_deletar_1, follow=True)
        
        # Verifica redirecionamento e mensagem de sucesso
        self.assertRedirects(response, self.url_listar)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(f'Serviço "{self.servico_1.nome}" excluído com sucesso.', str(messages[0]))
        
        # Verifica se o objeto foi removido
        self.assertEqual(Servico.objects.count(), 2)
        with self.assertRaises(Servico.DoesNotExist):
            Servico.objects.get(pk=self.servico_1.pk)