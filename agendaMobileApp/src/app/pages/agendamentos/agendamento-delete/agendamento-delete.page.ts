import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
  LoadingController,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButton,
  IonButtons,
  IonBackButton,
} from '@ionic/angular/standalone';
import { AgendamentosService } from '../../../services/agendamentos';

@Component({
  standalone: true,
  selector: 'app-agendamento-delete',
  templateUrl: './agendamento-delete.page.html',
  styleUrls: ['./agendamento-delete.page.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonButtons, IonBackButton],
})
export class AgendamentoDeletePage {
  id!: number;

  constructor(
    private route: ActivatedRoute,
    private agendamentosService: AgendamentosService,
    private router: Router,
    private loadingCtrl: LoadingController
  ) {
    this.id = Number(this.route.snapshot.paramMap.get('id'));
  }

  async confirm() {
    const loading = await this.loadingCtrl.create({ message: 'Removendo...' });
    await loading.present();
    this.agendamentosService.deleteAgendamento(this.id).subscribe({
      next: () => {
        loading.dismiss();
        this.router.navigate(['/agendamentos']);
      },
      error: (err) => {
        console.error(err);
        loading.dismiss();
      },
    });
  }

  cancel() {
    this.router.navigate(['/agendamentos']);
  }
}
