// src/app/app.routes.ts

import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  // 1. Rota de Login: Acesso livre
  {
    path: 'auth/login',
    loadComponent: () =>
      import('./pages/auth/login/login.page').then((m) => m.LoginPage),
  },

  // 2. Rotas de Páginas Protegidas - AGENDAMENTOS
  {
    path: 'agendamentos',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import(
        './pages/agendamentos/agendamento-list/agendamento-list.page'
      ).then((m) => m.AgendamentoListPage),
  },
  {
    path: 'agendamentos/novo',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import(
        './pages/agendamentos/agendamento-new/agendamento-new.page'
      ).then((m) => m.AgendamentoNewPage),
  },
  {
    path: 'agendamentos/editar/:id',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import(
        './pages/agendamentos/agendamento-edit/agendamento-edit.page'
      ).then((m) => m.AgendamentoEditPage),
  },
  {
    path: 'agendamentos/deletar/:id',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import(
        './pages/agendamentos/agendamento-delete/agendamento-delete.page'
      ).then((m) => m.AgendamentoDeletePage),
  },

  // Rotas de CLIENTES
  {
    path: 'clientes',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/clientes/cliente-list/cliente-list.page').then(
        (m) => m.ClienteListPage
      ),
  },
  {
    path: 'clientes/novo',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/clientes/cliente-new/cliente-new.page').then(
        (m) => m.ClienteNewPage
      ),
  },
  {
    path: 'clientes/editar/:id',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/clientes/cliente-edit/cliente-edit.page').then(
        (m) => m.ClienteEditPage
      ),
  },
  {
    path: 'clientes/deletar/:id',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/clientes/cliente-delete/cliente-delete.page').then(
        (m) => m.ClienteDeletePage
      ),
  },

  // Rotas de SERVIÇOS
  {
    path: 'servicos',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/servicos/servico-list/servico-list.page').then(
        (m) => m.ServicoListPage
      ),
  },
  {
    path: 'servicos/novo',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/servicos/servico-new/servico-new.page').then(
        (m) => m.ServicoNewPage
      ),
  },
  {
    path: 'servicos/editar/:id',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/servicos/servico-edit/servico-edit.page').then(
        (m) => m.ServicoEditPage
      ),
  },
  {
    path: 'servicos/deletar/:id',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/servicos/servico-delete/servico-delete.page').then(
        (m) => m.ServicoDeletePage
      ),
  },

  // Rota HOME/Dashboard
  {
    path: 'home',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./pages/home/home.page').then((m) => m.HomePage),
  },

  // 3. Rota Padrão: Redireciona para home após login
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full',
  },

  // 4. Fallback: qualquer outra rota desconhecida vai para home
  {
    path: '**',
    redirectTo: '/home',
  },
];