// src/app/services/servicos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface Servico {
  id: number;
  nome: string;
  descricao: string;
  duracao_minutos: number;
  preco: number;
}

@Injectable({
  providedIn: 'root'
})
export class ServicosService {
  private url = environment.apiUrl + 'servicos/';

  constructor(private http: HttpClient) {}

  getServicos(): Observable<Servico[]> {
    return this.http.get<any>(this.url).pipe(
      map(response => Array.isArray(response) ? response : (response?.results || []))
    );
  }

  getServico(id: number): Observable<Servico> {
    return this.http.get<Servico>(`${this.url}${id}/`);
  }

  createServico(payload: Partial<Servico>): Observable<Servico> {
    return this.http.post<Servico>(this.url, payload);
  }

  updateServico(id: number, payload: Partial<Servico>): Observable<Servico> {
    return this.http.put<Servico>(`${this.url}${id}/`, payload);
  }

  deleteServico(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}${id}/`);
  }
}
