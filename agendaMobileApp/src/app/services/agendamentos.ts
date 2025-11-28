// src/app/services/agendamentos.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment'; 

export interface Agendamento {
  id: number;
  cliente: number;
  cliente_nome: string; 
  servico: number;
  servico_nome: string;
  data_hora: string; 
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class AgendamentosService {
  private url = environment.apiUrl + 'agendamentos/';

  constructor(private http: HttpClient) {}

  getAgendamentos(): Observable<Agendamento[]> {
    return this.http.get<any>(this.url).pipe(
      map(response => {
        // Handle paginated response (DRF default) or direct array
        console.log('DEBUG AgendamentosService raw response:', response);
        return Array.isArray(response) ? response : (response?.results || []);
      })
    );
  }

  getAgendamento(id: number): Observable<Agendamento> {
    return this.http.get<Agendamento>(`${this.url}${id}/`);
  }

  createAgendamento(payload: Partial<Agendamento>): Observable<Agendamento> {
    return this.http.post<Agendamento>(this.url, payload);
  }

  updateAgendamento(id: number, payload: Partial<Agendamento>): Observable<Agendamento> {
    return this.http.put<Agendamento>(`${this.url}${id}/`, payload);
  }

  deleteAgendamento(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}${id}/`);
  }
}