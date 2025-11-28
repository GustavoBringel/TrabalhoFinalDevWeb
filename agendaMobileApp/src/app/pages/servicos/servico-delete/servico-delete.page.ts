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
import { ServicosService } from '../../../services/servicos';

@Component({
  standalone: true,
  selector: 'app-servico-delete',
  templateUrl: './servico-delete.page.html',
  styleUrls: ['./servico-delete.page.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonButtons, IonBackButton],
})
export class ServicoDeletePage {
  id!: number;

  constructor(
    private route: ActivatedRoute,
    private servicosService: ServicosService,
    private router: Router,
    private loadingCtrl: LoadingController
  ) {
    this.id = Number(this.route.snapshot.paramMap.get('id'));
  }

  async confirm() {
    const loading = await this.loadingCtrl.create({ message: 'Removendo...' });
    await loading.present();
    this.servicosService.deleteServico(this.id).subscribe({
      next: () => {
        loading.dismiss();
        this.router.navigate(['/servicos']);
      },
      error: (err) => {
        console.error(err);
        loading.dismiss();
      },
    });
  }

  cancel() {
    this.router.navigate(['/servicos']);
  }
}
