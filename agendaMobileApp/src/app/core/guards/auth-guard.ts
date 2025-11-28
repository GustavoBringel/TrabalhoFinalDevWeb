// src/app/core/guards/auth.guard.ts

import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs'; // Keep Observable for types if needed elsewhere, but focus on Promise for canActivate
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService: AuthService, 
    private router: Router
  ) {}

  async canActivate(): Promise<boolean | UrlTree> {
    // Verifica se o usuário tem um Token armazenado (usando o método assíncrono para Ionic Storage)
    const token = await this.authService.getTokenAsync();

    // Debug: registrar estado do token e decisão do guard
    console.log('[AuthGuard] token present (async)?', !!token, 'token:', token ? 'exists' : 'null');

    if (token) {
      console.log('[AuthGuard] allow navigation (async)');
      return true;
    }

    console.log('[AuthGuard] returning UrlTree to /auth/login (async)');
    // Retorna um UrlTree para redirecionamento
    return this.router.createUrlTree(['/auth/login']);
  }
}