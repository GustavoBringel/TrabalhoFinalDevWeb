# agendamentos/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date 
from django.contrib.messages import get_messages
from django.conf import settings 

# Importando Modelos (Ajuste os imports se os nomes das suas apps forem diferentes)
from clientes.models import Cliente 
from servicos.models import Servico 
from .models import Agendamento
from django.contrib.auth.models import User 


# ======================================================================
# 1. TESTES DE VALIDAÇÃO (VIEW: novo_editar_agendamento)
# ======================================================================

class AgendamentoValidationTest(TestCase):
    """
    Testa as regras de validação da View novo_editar_agendamento:
    Passado, Antecedência de 30 minutos, Conflito de Horário e Bypass de Edição.
    """
    def setUp(self):
        # 1. Configuração de Usuário e Login
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # 2. Configuração de Dados Base
        self.cliente = Cliente.objects.create(nome='Cliente Teste Validação')
        self.outro_cliente = Cliente.objects.create(nome='Cliente Conflito')
        # Serviço com 60 minutos (1 hora) de duração
        self.servico_60 = Servico.objects.create(nome='Corte', duracao_minutos=60, preco=50.00)
        # Serviço com 30 minutos de duração
        self.servico_30 = Servico.objects.create(nome='Barba', duracao_minutos=30, preco=30.00)

        # 3. Configuração de URLs e Horários
        self.url_novo = reverse('cadastrar-agendamento')

        # Horário de referência (agora + 1 hora, para ser um horário válido)
        self.horario_valido = timezone.now() + timedelta(hours=1)
        # Remove segundos e microssegundos para corresponder ao formato do formulário
        self.horario_valido = self.horario_valido.replace(second=0, microsecond=0)
        
        # 4. Dados POST Válidos
        self.dados_validos = {
            'cliente': self.cliente.pk,
            'servico': self.servico_60.pk,
            'data_hora': self.horario_valido.strftime('%Y-%m-%dT%H:%M'),
            'status': 'AGENDADO',
        }

        # 5. Cria Agendamento Existente (para checagem de conflito e edição)
        # Agendamento A: Começa em H+2, dura 60 min (termina em H+3)
        self.horario_existente = self.horario_valido + timedelta(hours=1)
        self.agendamento_existente = Agendamento.objects.create(
            cliente=self.outro_cliente,
            servico=self.servico_60,
            data_hora=self.horario_existente, 
            status='AGENDADO'
        )
        self.url_editar_existente = reverse('editar-agendamento', args=[self.agendamento_existente.pk])


# --- TESTES DE VALIDAÇÃO DE TEMPO (A e B da View) ---

    def test_1_agendamento_passado_invalido(self):
        """Não deve permitir agendar em um horário que já passou."""
        horario_passado = timezone.now() - timedelta(minutes=10)
        dados = self.dados_validos.copy()
        dados['data_hora'] = horario_passado.strftime('%Y-%m-%dT%H:%M')
        
        response = self.client.post(self.url_novo, dados, follow=True)
        
        # Deve falhar o cadastro e mostrar a mensagem de erro
        self.assertContains(response, 'Não é possível agendar em um horário que já passou.')
        self.assertEqual(Agendamento.objects.count(), 1) # Apenas o existente

    def test_2_agendamento_sem_antecedencia_invalido(self):
        """Deve exigir 30 minutos de antecedência."""
        # Tenta agendar para agora + 15 minutos (sem antecedência suficiente)
        horario_sem_antecedencia = timezone.now() + timedelta(minutes=15)
        dados = self.dados_validos.copy()
        dados['data_hora'] = horario_sem_antecedencia.strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(self.url_novo, dados, follow=True)
        
        self.assertContains(response, 'Agendamentos devem ter no mínimo 30 minutos de antecedência.')
        self.assertEqual(Agendamento.objects.count(), 1)


# --- TESTES DE VALIDAÇÃO DE CONFLITO (C da View) ---

    def test_3_agendamento_conflito_invalido_sobreposicao(self):
        """Não deve permitir agendar um serviço que se sobrepõe ao existente (H+2 a H+3)."""
        
        # Novo Agendamento (Serviço de 60 min): Tenta começar em H+2:30 (conflito)
        horario_conflito = self.agendamento_existente.data_hora + timedelta(minutes=30)
        dados = self.dados_validos.copy()
        dados['data_hora'] = horario_conflito.strftime('%Y-%m-%dT%H:%M')
        
        response = self.client.post(self.url_novo, dados, follow=True)
        
        self.assertContains(response, 'Conflito de horários!')
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_4_agendamento_valido_intervalo_seguro(self):
        """Deve permitir agendar se o horário for imediatamente após o término."""
        # Existente (H+2 a H+3). Novo (Começa em H+3:01).
        horario_seguro = self.agendamento_existente.data_hora + timedelta(minutes=61)
        dados = self.dados_validos.copy()
        dados['servico'] = self.servico_30.pk
        dados['data_hora'] = horario_seguro.strftime('%Y-%m-%dT%H:%M')
        
        response = self.client.post(self.url_novo, dados, follow=True)
        
        self.assertContains(response, 'Novo agendamento criado com sucesso!')
        self.assertEqual(Agendamento.objects.count(), 2) # Existente + Novo

    def test_5_agendamento_conflito_com_agendamento_cancelado_deve_ser_valido(self):
        """Deve ignorar agendamentos com status CANCELADO na checagem de conflito."""
        # Cancela o agendamento existente
        self.agendamento_existente.status = 'CANCELADO'
        self.agendamento_existente.save()

        # Novo Agendamento (Tenta começar em H+2:30, que antes conflitava)
        horario_conflito_liberado = self.agendamento_existente.data_hora + timedelta(minutes=30)
        dados = self.dados_validos.copy()
        dados['data_hora'] = horario_conflito_liberado.strftime('%Y-%m-%dT%H:%M')
        
        response = self.client.post(self.url_novo, dados, follow=True)
        
        self.assertContains(response, 'Novo agendamento criado com sucesso!')
        self.assertEqual(Agendamento.objects.count(), 2) # Existente (Cancelado) + Novo (Agendado)


    def test_7_edicao_com_mudanca_hora_e_conflito_deve_falhar(self):
        """Se a hora for mudada, a checagem de conflito deve ser ativada e falhar."""
        # Existente (self.agendamento_existente): H+2 a H+3 (60 min)
        
        # Cria um novo agendamento B (H+4 a H+5)
        agendamento_b = Agendamento.objects.create(
            cliente=self.cliente,
            servico=self.servico_60,
            data_hora=self.horario_existente + timedelta(hours=2), 
            status='AGENDADO'
        )
        url_editar_b = reverse('editar-agendamento', args=[agendamento_b.pk])

        # Tenta editar o Agendamento B para começar em H+2:30 (conflitando com self.agendamento_existente)
        horario_conflito = self.agendamento_existente.data_hora + timedelta(minutes=30)
        
        dados_edicao = {
            'cliente': agendamento_b.cliente.pk,
            'servico': agendamento_b.servico.pk,
            'data_hora': horario_conflito.strftime('%Y-%m-%dT%H:%M'), # Hora que causa conflito
            'status': 'CONFIRMADO', 
        }

        response = self.client.post(url_editar_b, dados_edicao, follow=True)

        self.assertContains(response, 'Conflito de horários!')
        
        # Verifica se o horário original de B não foi alterado
        agendamento_b_nao_alterado = Agendamento.objects.get(pk=agendamento_b.pk)
        self.assertEqual(agendamento_b_nao_alterado.data_hora, agendamento_b.data_hora)


# ======================================================================
# 2. TESTES DE CRUD (VIEWS: listar_agendamentos, deletar_agendamento)
# ======================================================================

class AgendamentoCRUDTest(TestCase):
    """
    Testes para as views de Listagem, Busca e Deleção de Agendamentos.
    """
    def setUp(self):
        # 1. Configuração de Usuário e Login
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # 2. Configuração de Dados Base
        self.cliente_a = Cliente.objects.create(nome='João Silva')
        self.cliente_b = Cliente.objects.create(nome='Maria Oliveira')
        self.servico_corte = Servico.objects.create(nome='Corte de Cabelo', duracao_minutos=60, preco=50.00)
        self.servico_pe = Servico.objects.create(nome='Pé e Mão', duracao_minutos=45, preco=40.00)

        # 3. Configuração de Horários (Hoje, Amanhã e Passado)
        hoje = timezone.localdate()
        amanha = hoje + timedelta(days=1)
        passado = hoje - timedelta(days=1)
        
        # Garante que o horário é futuro em relação ao NOW do teste e está ciente de timezone
        horario_agora = timezone.now().replace(second=0, microsecond=0) + timedelta(minutes=60) 

        # Agendamento 1: HOJE (Deve aparecer na lista. Status: AGENDADO)
        self.agendamento_hoje_a = Agendamento.objects.create(
            cliente=self.cliente_a,
            servico=self.servico_corte,
            data_hora=horario_agora + timedelta(hours=1),
            status='AGENDADO',
        )
        
        # Agendamento 2: HOJE (Deve aparecer na lista. Status: CANCELADO)
        self.agendamento_hoje_cancelado = Agendamento.objects.create(
            cliente=self.cliente_b,
            servico=self.servico_pe,
            data_hora=horario_agora + timedelta(hours=2),
            status='CANCELADO',
        )
        
        # Agendamento 3: AMANHÃ (Deve aparecer na lista. Status: AGENDADO)
        self.agendamento_amanha = Agendamento.objects.create(
            cliente=self.cliente_a,
            servico=self.servico_pe,
            data_hora=horario_agora.replace(year=amanha.year, month=amanha.month, day=amanha.day),
            status='AGENDADO',
        )
        
        # Agendamento 4: PASSADO (Não deve aparecer na lista padrão. Status: CONCLUIDO)
        self.agendamento_passado = Agendamento.objects.create(
            cliente=self.cliente_b,
            servico=self.servico_corte,
            data_hora=horario_agora.replace(year=passado.year, month=passado.month, day=passado.day),
            status='CONCLUIDO'
        )
        
        # 4. Configuração de URLs
        self.url_listar = reverse('listar-agendamentos')
        self.url_deletar_hoje_a = reverse('deletar-agendamento', args=[self.agendamento_hoje_a.pk])


# --- TESTES DE LISTAGEM E CONTAGENS ---

    def test_8_listar_agendamentos_status_code(self):
        """Verifica se a view listar_agendamentos carrega corretamente."""
        response = self.client.get(self.url_listar)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agendamentos/listar.html')
        
    def test_9_listar_agendamentos_filtro_data_correto(self):
        """A lista deve mostrar apenas agendamentos a partir de hoje."""
        response = self.client.get(self.url_listar)
        agendamentos_context = response.context['agendamentos']
        
        # Agendamentos que devem aparecer (A1, A2, A3) = 3
        self.assertEqual(len(agendamentos_context), 3) 
        
        # Verifica se o agendamento no passado (A4) FOI excluído
        self.assertNotIn(self.agendamento_passado, agendamentos_context)

    def test_10_listar_agendamentos_contagens_corretas(self):
        """Verifica se o total de hoje e pendentes estão corretos."""
        response = self.client.get(self.url_listar)
        
        # Total Hoje (Filtro GTE hoje, apenas dia de hoje): A1 (AGENDADO) + A2 (CANCELADO) = 2
        self.assertEqual(response.context['total_hoje'], 2)
        
        # Total Pendente (Status 'AGENDADO' na lista): A1 (Hoje) + A3 (Amanhã) = 2
        self.assertEqual(response.context['total_pendente'], 2)

    def test_11_listar_agendamentos_busca_por_cliente(self):
        """Deve filtrar agendamentos pelo nome do cliente (João)."""
        response = self.client.get(self.url_listar + '?q=João')
        agendamentos_context = response.context['agendamentos']
        
        # Agendamentos do João a partir de hoje: A1 (Hoje, AGENDADO) e A3 (Amanhã, AGENDADO)
        self.assertEqual(len(agendamentos_context), 2)
        self.assertIn(self.agendamento_hoje_a, agendamentos_context)

    def test_12_listar_agendamentos_busca_por_servico(self):
        """Deve filtrar agendamentos pelo nome do serviço (Pé)."""
        response = self.client.get(self.url_listar + '?q=Pé')
        agendamentos_context = response.context['agendamentos']
        
        # Agendamentos com "Pé e Mão": A2 (Hoje) e A3 (Amanhã)
        self.assertEqual(len(agendamentos_context), 2)
        self.assertIn(self.agendamento_hoje_cancelado, agendamentos_context)


# --- TESTES DE DELEÇÃO (CORRIGIDO) ---

    def test_13_deletar_agendamento_get(self):
        """Verifica se a view de deleção (GET) carrega a confirmação."""
        response = self.client.get(self.url_deletar_hoje_a)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agendamentos/confirm_delete.html')
        
        # CORREÇÃO: A string real no HTML é "Cliente: João Silva" (sem o prefixo "Agendamento do cliente")
        self.assertContains(response, f'Cliente: {self.agendamento_hoje_a.cliente.nome}') 

    def test_14_deletar_agendamento_post_sucesso(self):
        """Deve excluir o agendamento e redirecionar com mensagem de sucesso."""
        
        # Contagem inicial (4 total)
        self.assertEqual(Agendamento.objects.count(), 4)
        
        response = self.client.post(self.url_deletar_hoje_a, follow=True)
        
        # Verifica mensagem de sucesso
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(f'Agendamento do cliente {self.cliente_a.nome} excluído com sucesso.', str(messages[0]))
        
        # Verifica se o objeto foi removido e a contagem diminuiu
        self.assertEqual(Agendamento.objects.count(), 3)
        with self.assertRaises(Agendamento.DoesNotExist):
            Agendamento.objects.get(pk=self.agendamento_hoje_a.pk)