// src/app/core/interceptors/token.interceptor.ts

import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable, from } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth.service'; // Ajuste este caminho se necessário
import { environment } from '../../../environments/environment'; // Ajuste este caminho se necessário

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    
    // Use the async token getter which returns a Promise
    return from(this.authService.getTokenAsync()).pipe(

      switchMap(token => {
        const isApiUrl = request.url.startsWith(environment.apiUrl);
        const isLoginRequest = request.url.includes('token-auth');

        if (token && isApiUrl && !isLoginRequest) {
          
          // Anexa o Token no formato do Django: 'Token SEU_TOKEN_AQUI'
          const clonedReq = request.clone({
            headers: request.headers.set('Authorization', `Token ${token}`)
          });
          return next.handle(clonedReq);
        } else {
          // Passa a requisição original
          return next.handle(request);
        }
      })
    );
  }
}