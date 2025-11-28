// src/app/pages/agendamentos/agendamento-new/agendamento-new.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { AgendamentosService } from '../../../services/agendamentos';
import { ClientesService, Cliente } from '../../../services/clientes';
import { ServicosService, Servico } from '../../../services/servicos';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-agendamento-new',
  templateUrl: './agendamento-new.page.html',
  styleUrls: ['./agendamento-new.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule, RouterModule]
})
export class AgendamentoNewPage implements OnInit {
  agendamentoForm: FormGroup;
  clientes$: Observable<Cliente[]>;
  servicos$: Observable<Servico[]>;

  constructor(
    private fb: FormBuilder,
    private agendamentosService: AgendamentosService,
    private clientesService: ClientesService,
    private servicosService: ServicosService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.agendamentoForm = this.fb.group({
      cliente: ['', Validators.required],
      servico: ['', Validators.required],
      data_hora: ['', Validators.required],
      status: ['AGENDADO', Validators.required]
    });
    this.clientes$ = new Observable<Cliente[]>();
    this.servicos$ = new Observable<Servico[]>();
  }

  ngOnInit() {
    this.clientes$ = this.clientesService.getClientes();
    this.servicos$ = this.servicosService.getServicos();
  }

  createAgendamento() {
    if (this.agendamentoForm.invalid) {
      this.presentToast('Por favor, preencha todos os campos.');
      return;
    }

    this.agendamentosService.createAgendamento(this.agendamentoForm.value).subscribe({
      next: () => {
        this.presentToast('Agendamento criado com sucesso.');
        this.router.navigate(['/agendamentos']);
      },
      error: (err) => {
        console.error('Erro ao criar agendamento:', err);
        this.presentToast('Erro ao criar agendamento.');
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