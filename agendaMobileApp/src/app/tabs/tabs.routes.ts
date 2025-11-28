import { Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

export const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      {
        path: 'tab1',
        loadComponent: () =>
          import('../pages/agendamentos/agendamento-list/agendamento-list.page').then(
            (m) => m.AgendamentoListPage
          ),
      },
      {
        path: 'tab2',
        loadComponent: () =>
          import('../pages/clientes/cliente-list/cliente-list.page').then(
            (m) => m.ClienteListPage
          ),
      },
      {
        path: 'tab3',
        loadComponent: () =>
          import('../pages/servicos/servico-list/servico-list.page').then(
            (m) => m.ServicoListPage
          ),
      },
      {
        path: '',
        redirectTo: '/tabs/tab1',
        pathMatch: 'full',
      },
    ],
  },
  {
    path: '',
    redirectTo: '/tabs/tab1',
    pathMatch: 'full',
  },
];
