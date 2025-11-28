// src/app/pages/agendamentos/agendamento-edit/agendamento-edit.page.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { AgendamentosService } from '../../../services/agendamentos';
import { ClientesService, Cliente } from '../../../services/clientes';
import { ServicosService, Servico } from '../../../services/servicos';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-agendamento-edit',
  templateUrl: './agendamento-edit.page.html',
  styleUrls: ['./agendamento-edit.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule, RouterModule]
})
export class AgendamentoEditPage implements OnInit {
  agendamentoForm: FormGroup;
  agendamentoId: number = 0;
  clientes$: Observable<Cliente[]>;
  servicos$: Observable<Servico[]>;

  constructor(
    private fb: FormBuilder,
    private agendamentosService: AgendamentosService,
    private clientesService: ClientesService,
    private servicosService: ServicosService,
    private router: Router,
    private route: ActivatedRoute,
    private toastController: ToastController
  ) {
    this.agendamentoForm = this.fb.group({
      cliente: ['', Validators.required],
      servico: ['', Validators.required],
      data_hora: ['', Validators.required],
      status: ['', Validators.required]
    });
    this.clientes$ = new Observable<Cliente[]>();
    this.servicos$ = new Observable<Servico[]>();
  }

  ngOnInit() {
    this.clientes$ = this.clientesService.getClientes();
    this.servicos$ = this.servicosService.getServicos();

    this.agendamentoId = +(this.route.snapshot.paramMap.get('id') || 0);
    if (this.agendamentoId) {
      this.agendamentosService.getAgendamento(this.agendamentoId).subscribe(agendamento => {
        this.agendamentoForm.patchValue(agendamento);
      });
    }
  }

  updateAgendamento() {
    if (this.agendamentoForm.invalid) {
      this.presentToast('Por favor, preencha todos os campos.');
      return;
    }

    this.agendamentosService.updateAgendamento(this.agendamentoId, this.agendamentoForm.value).subscribe({
      next: () => {
        this.presentToast('Agendamento atualizado com sucesso.');
        this.router.navigate(['/agendamentos']);
      },
      error: (err) => {
        console.error('Erro ao atualizar agendamento:', err);
        this.presentToast('Erro ao atualizar agendamento.');
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