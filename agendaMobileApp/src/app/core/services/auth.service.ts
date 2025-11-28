// src/app/core/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { Storage } from '@ionic/storage-angular';

export interface AuthResponse {
  token: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authUrl = environment.apiUrl + 'token-auth/';
  private tokenKey = 'auth_token';
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasToken());

  // Ionic Storage instance (for native apps)
  private storageInstance: Storage | null = null;

  constructor(private http: HttpClient, private storage: Storage) {
    // initialize Ionic storage for native persistence
    this.initStorage();
  }

  private async initStorage() {
    try {
      this.storageInstance = await this.storage.create();
    } catch (e) {
      // ignore storage init errors; fallback to localStorage
      this.storageInstance = null;
    }
  }

  login(credentials: {username: string, password: string}): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(this.authUrl, credentials).pipe(
      tap(response => {
        // persist token both in localStorage (sync) and Ionic Storage (async)
        this.setToken(response.token);
        this.setTokenAsync(response.token);
        this.isAuthenticatedSubject.next(true);
      })
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.removeTokenAsync();
    this.isAuthenticatedSubject.next(false);
  }

  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  /**
   * Synchronous getter (for guards/interceptors running in browser)
   */
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Async getter for native storage (recommended for mobile builds)
   */
  async getTokenAsync(): Promise<string | null> {
    try {
      if (this.storageInstance) {
        const v = await this.storageInstance.get(this.tokenKey);
        return v ?? null;
      }
    } catch (e) {
      // ignore
    }
    return this.getToken();
  }

  async setTokenAsync(token: string): Promise<void> {
    try {
      if (this.storageInstance) {
        await this.storageInstance.set(this.tokenKey, token);
      }
    } catch (e) {
      // ignore
    }
  }

  async removeTokenAsync(): Promise<void> {
    try {
      if (this.storageInstance) {
        await this.storageInstance.remove(this.tokenKey);
      }
    } catch (e) {
      // ignore
    }
  }

  hasToken(): boolean {
    return !!this.getToken();
  }

  isAuthenticated(): Observable<boolean> {
    return this.isAuthenticatedSubject.asObservable();
  }
}
