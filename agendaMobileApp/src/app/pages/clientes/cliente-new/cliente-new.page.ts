// src/app/pages/clientes/cliente-new/cliente-new.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { ClientesService } from '../../../services/clientes';

@Component({
  selector: 'app-cliente-new',
  templateUrl: './cliente-new.page.html',
  styleUrls: ['./cliente-new.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule, RouterModule]
})
export class ClienteNewPage implements OnInit {
  clienteForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private clientesService: ClientesService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.clienteForm = this.fb.group({
      nome: ['', Validators.required],
      telefone: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  ngOnInit() {}

  createCliente() {
    if (this.clienteForm.invalid) {
      this.presentToast('Por favor, preencha todos os campos corretamente.');
      return;
    }

    this.clientesService.createCliente(this.clienteForm.value).subscribe({
      next: () => {
        this.presentToast('Cliente criado com sucesso.');
        this.router.navigate(['/clientes']);
      },
      error: (err) => {
        console.error('Erro ao criar cliente:', err);
        this.presentToast('Erro ao criar cliente.');
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