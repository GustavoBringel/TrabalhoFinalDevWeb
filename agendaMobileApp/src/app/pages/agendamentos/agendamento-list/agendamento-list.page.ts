// src/app/pages/agendamentos/agendamento-list/agendamento-list.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule, ToastController } from '@ionic/angular';
import { Router, RouterModule } from '@angular/router';
import { AgendamentosService, Agendamento } from '../../../services/agendamentos';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-agendamento-list',
  templateUrl: './agendamento-list.page.html',
  styleUrls: ['./agendamento-list.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule]
})
export class AgendamentoListPage implements OnInit {
  agendamentos$: Observable<Agendamento[]>;

  constructor(
    private agendamentosService: AgendamentosService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.agendamentos$ = new Observable<Agendamento[]>();
  }

  ngOnInit() {
    this.loadAgendamentos();
  }

  loadAgendamentos() {
    this.agendamentos$ = this.agendamentosService.getAgendamentos();
  }

  editAgendamento(id: number) {
    this.router.navigate(['/agendamentos/editar', id]);
  }

  deleteAgendamento(id: number) {
    this.agendamentosService.deleteAgendamento(id).subscribe({
      next: () => {
        this.presentToast('Agendamento excluído com sucesso.');
        this.loadAgendamentos();
      },
      error: (err) => {
        console.error('Erro ao excluir agendamento:', err);
        this.presentToast('Erro ao excluir agendamento.');
      }
    });
  }

  async presentToast(message: string) {
    const toast = await this.toastController.create({
      message: message,
      duration: 2000,
      position: 'top'
    });
    toast.present();
  }
}
