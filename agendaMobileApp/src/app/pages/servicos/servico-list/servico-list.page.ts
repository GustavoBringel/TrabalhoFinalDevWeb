// src/app/pages/servicos/servico-list/servico-list.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule, ToastController } from '@ionic/angular';
import { Router, RouterModule } from '@angular/router';
import { ServicosService, Servico } from '../../../services/servicos.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-servico-list',
  templateUrl: './servico-list.page.html',
  styleUrls: ['./servico-list.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule]
})
export class ServicoListPage implements OnInit {
  servicos$: Observable<Servico[]>;

  constructor(
    private servicosService: ServicosService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.servicos$ = new Observable<Servico[]>();
  }

  ngOnInit() {
    this.loadServicos();
  }

  loadServicos() {
    this.servicos$ = this.servicosService.getServicos();
  }

  editServico(id: number) {
    this.router.navigate(['/servicos/editar', id]);
  }

  deleteServico(id: number) {
    this.servicosService.deleteServico(id).subscribe({
      next: () => {
        this.presentToast('Serviço excluído com sucesso.');
        this.loadServicos();
      },
      error: (err) => {
        console.error('Erro ao excluir serviço:', err);
        this.presentToast('Erro ao excluir serviço.');
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