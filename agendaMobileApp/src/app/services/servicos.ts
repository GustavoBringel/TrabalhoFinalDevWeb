import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface Servico {
  id: number;
  nome: string;
  descricao: string;
  preco: number;
  duracao_minutos: number;
}

@Injectable({
  providedIn: 'root',
})
export class ServicosService {
  private url = environment.apiUrl + 'servicos/';

  constructor(private http: HttpClient) {}

  getServicos(): Observable<Servico[]> {
    return this.http.get<any>(this.url).pipe(
      map(response => {
        // Handle paginated response (DRF default) or direct array
        console.log('DEBUG ServicosService raw response:', response);
        return Array.isArray(response) ? response : (response?.results || []);
      })
    );
  }

  getServico(id: number): Observable<Servico> {
    return this.http.get<Servico>(`${this.url}${id}/`);
  }

  createServico(servico: Partial<Servico>): Observable<Servico> {
    return this.http.post<Servico>(this.url, servico);
  }

  updateServico(id: number, servico: Partial<Servico>): Observable<Servico> {
    return this.http.put<Servico>(`${this.url}${id}/`, servico);
  }

  deleteServico(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}${id}/`);
  }
}
