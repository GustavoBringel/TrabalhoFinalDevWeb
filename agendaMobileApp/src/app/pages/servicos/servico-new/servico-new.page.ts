// src/app/pages/servicos/servico-new/servico-new.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { ServicosService } from '../../../services/servicos';

@Component({
  selector: 'app-servico-new',
  templateUrl: './servico-new.page.html',
  styleUrls: ['./servico-new.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule, RouterModule]
})
export class ServicoNewPage implements OnInit {
  servicoForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private servicosService: ServicosService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.servicoForm = this.fb.group({
      nome: ['', Validators.required],
      descricao: [''],
      duracao_minutos: ['', [Validators.required, Validators.min(1)]],
      preco: ['', [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit() {}

  createServico() {
    if (this.servicoForm.invalid) {
      this.presentToast('Por favor, preencha todos os campos corretamente.');
      return;
    }

    this.servicosService.createServico(this.servicoForm.value).subscribe({
      next: () => {
        this.presentToast('Serviço criado com sucesso.');
        this.router.navigate(['/servicos']);
      },
      error: (err) => {
        console.error('Erro ao criar serviço:', err);
        this.presentToast('Erro ao criar serviço.');
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