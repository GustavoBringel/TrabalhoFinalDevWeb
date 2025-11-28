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
import { ClientesService } from '../../../services/clientes';

@Component({
  standalone: true,
  selector: 'app-cliente-delete',
  templateUrl: './cliente-delete.page.html',
  styleUrls: ['./cliente-delete.page.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonButtons, IonBackButton],
})
export class ClienteDeletePage {
  id!: number;

  constructor(
    private route: ActivatedRoute,
    private clientesService: ClientesService,
    private router: Router,
    private loadingCtrl: LoadingController
  ) {
    this.id = Number(this.route.snapshot.paramMap.get('id'));
  }

  async confirm() {
    const loading = await this.loadingCtrl.create({ message: 'Removendo...' });
    await loading.present();
    this.clientesService.deleteCliente(this.id).subscribe({
      next: () => {
        loading.dismiss();
        this.router.navigate(['/clientes']);
      },
      error: (err) => {
        console.error(err);
        loading.dismiss();
      },
    });
  }

  cancel() {
    this.router.navigate(['/clientes']);
  }
}
