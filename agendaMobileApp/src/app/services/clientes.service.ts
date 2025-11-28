// src/app/services/clientes.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface Cliente {
  id: number;
  nome: string;
  telefone: string;
  email: string;
}

@Injectable({
  providedIn: 'root'
})
export class ClientesService {
  private url = environment.apiUrl + 'clientes/';

  constructor(private http: HttpClient) {}

  getClientes(): Observable<Cliente[]> {
    return this.http.get<any>(this.url).pipe(
      map(response => Array.isArray(response) ? response : (response?.results || []))
    );
  }

  getCliente(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.url}${id}/`);
  }

  createCliente(payload: Partial<Cliente>): Observable<Cliente> {
    return this.http.post<Cliente>(this.url, payload);
  }

  updateCliente(id: number, payload: Partial<Cliente>): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.url}${id}/`, payload);
  }

  deleteCliente(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}${id}/`);
  }
}
