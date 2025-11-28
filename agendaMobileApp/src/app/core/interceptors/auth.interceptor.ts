// src/app/core/interceptors/auth.interceptor.ts
import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, from } from 'rxjs'; // Import 'from'
import { catchError, switchMap } from 'rxjs/operators'; // Import 'switchMap'
import { AuthService } from '../services/auth.service';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService, private router: Router) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // Use from() to convert the Promise from getTokenAsync() to an Observable
    return from(this.authService.getTokenAsync()).pipe(
      switchMap(token => {
        const isApiUrl = request.url.startsWith(environment.apiUrl);
        const isLoginRequest = request.url.includes('token-auth');

        let modifiedRequest = request;

        // Only attach token for our API (and not for the login request)
        if (token && isApiUrl && !isLoginRequest) {
          modifiedRequest = request.clone({ headers: request.headers.set('Authorization', 'Token ' + token) });
        }

        // Capture 401/403 and force logout + redirect to login
        return next.handle(modifiedRequest).pipe(
          catchError((err: unknown) => {
            if (err instanceof HttpErrorResponse) {
              if (err.status === 401 || err.status === 403) {
                console.warn('[AuthInterceptor] Unauthorized, logging out and redirecting to login');
                this.authService.logout();
                try {
                  this.router.navigate(['/auth/login']);
                } catch (e) {
                  // noop
                }
              }
            }
            return throwError(() => err);
          })
        );
      })
    );
  }
}
