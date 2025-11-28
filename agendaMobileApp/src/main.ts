// src/main.ts

import { enableProdMode, importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { RouteReuseStrategy, provideRouter } from '@angular/router';

// 💥 LINHA CORRETA PADRÃO (Apenas certifique-se de que a reinstalação resolve o erro)
import { IonicRouteStrategy } from '@ionic/angular'; 
import { provideIonicAngular } from '@ionic/angular/standalone';

// 💥 NOVOS IMPORTS DE HTTP
import { HTTP_INTERCEPTORS, provideHttpClient } from '@angular/common/http';
import { withInterceptorsFromDi } from '@angular/common/http'; 

// 💥 IMPORT DO SEU INTERCEPTOR (Verifique se o caminho está correto: ./app/core/...)
import { AuthInterceptor } from './app/core/interceptors/auth.interceptor'; 

// 💥 IMPORT DO STORAGE (Se estiver usando)
import { IonicStorageModule } from '@ionic/storage-angular'; 


import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';
import { environment } from './environments/environment';

if (environment.production) {
  enableProdMode();
}

bootstrapApplication(AppComponent, {
  providers: [
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(),
    provideRouter(routes),

    // Habilita o uso de Storage
    importProvidersFrom(IonicStorageModule.forRoot()),
    
    // Configuração para HTTP e Interceptores
    provideHttpClient(
      withInterceptorsFromDi() 
    ),
    
    // REGISTRO DO SEU INTERCEPTOR
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
});