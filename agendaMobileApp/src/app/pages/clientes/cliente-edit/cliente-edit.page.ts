// src/app/pages/clientes/cliente-edit/cliente-edit.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { ClientesService } from '../../../services/clientes';

@Component({
  selector: 'app-cliente-edit',
  templateUrl: './cliente-edit.page.html',
  styleUrls: ['./cliente-edit.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule, RouterModule]
})
export class ClienteEditPage implements OnInit {
  clienteForm: FormGroup;
  clienteId: number = 0;

  constructor(
    private fb: FormBuilder,
    private clientesService: ClientesService,
    private router: Router,
    private route: ActivatedRoute,
    private toastController: ToastController
  ) {
    this.clienteForm = this.fb.group({
      nome: ['', Validators.required],
      telefone: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  ngOnInit() {
    this.clienteId = +(this.route.snapshot.paramMap.get('id') || 0);
    if (this.clienteId) {
      this.clientesService.getCliente(this.clienteId).subscribe(cliente => {
        this.clienteForm.patchValue(cliente);
      });
    }
  }

  updateCliente() {
    if (this.clienteForm.invalid) {
      this.presentToast('Por favor, preencha todos os campos corretamente.');
      return;
    }

    this.clientesService.updateCliente(this.clienteId, this.clienteForm.value).subscribe({
      next: () => {
        this.presentToast('Cliente atualizado com sucesso.');
        this.router.navigate(['/clientes']);
      },
      error: (err) => {
        console.error('Erro ao atualizar cliente:', err);
        this.presentToast('Erro ao atualizar cliente.');
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