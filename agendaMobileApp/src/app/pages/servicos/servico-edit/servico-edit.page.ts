// src/app/pages/servicos/servico-edit/servico-edit.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { ServicosService } from '../../../services/servicos';

@Component({
  selector: 'app-servico-edit',
  templateUrl: './servico-edit.page.html',
  styleUrls: ['./servico-edit.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule, RouterModule]
})
export class ServicoEditPage implements OnInit {
  servicoForm: FormGroup;
  servicoId: number = 0;

  constructor(
    private fb: FormBuilder,
    private servicosService: ServicosService,
    private router: Router,
    private route: ActivatedRoute,
    private toastController: ToastController
  ) {
    this.servicoForm = this.fb.group({
      nome: ['', Validators.required],
      descricao: [''],
      duracao_minutos: ['', [Validators.required, Validators.min(1)]],
      preco: ['', [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit() {
    this.servicoId = +(this.route.snapshot.paramMap.get('id') || 0);
    if (this.servicoId) {
      this.servicosService.getServico(this.servicoId).subscribe(servico => {
        this.servicoForm.patchValue(servico);
      });
    }
  }

  updateServico() {
    if (this.servicoForm.invalid) {
      this.presentToast('Por favor, preencha todos os campos corretamente.');
      return;
    }

    this.servicosService.updateServico(this.servicoId, this.servicoForm.value).subscribe({
      next: () => {
        this.presentToast('Serviço atualizado com sucesso.');
        this.router.navigate(['/servicos']);
      },
      error: (err) => {
        console.error('Erro ao atualizar serviço:', err);
        this.presentToast('Erro ao atualizar serviço.');
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