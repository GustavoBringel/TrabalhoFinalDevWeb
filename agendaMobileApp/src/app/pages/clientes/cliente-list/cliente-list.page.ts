// src/app/pages/clientes/cliente-list/cliente-list.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule, ToastController } from '@ionic/angular';
import { Router, RouterModule } from '@angular/router';
import { ClientesService, Cliente } from '../../../services/clientes.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-cliente-list',
  templateUrl: './cliente-list.page.html',
  styleUrls: ['./cliente-list.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule]
})
export class ClienteListPage implements OnInit {
  clientes$: Observable<Cliente[]>;

  constructor(
    private clientesService: ClientesService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.clientes$ = new Observable<Cliente[]>();
  }

  ngOnInit() {
    this.loadClientes();
  }

  loadClientes() {
    this.clientes$ = this.clientesService.getClientes();
  }

  editCliente(id: number) {
    this.router.navigate(['/clientes/editar', id]);
  }

  deleteCliente(id: number) {
    this.clientesService.deleteCliente(id).subscribe({
      next: () => {
        this.presentToast('Cliente excluído com sucesso.');
        this.loadClientes();
      },
      error: (err) => {
        console.error('Erro ao excluir cliente:', err);
        this.presentToast('Erro ao excluir cliente.');
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