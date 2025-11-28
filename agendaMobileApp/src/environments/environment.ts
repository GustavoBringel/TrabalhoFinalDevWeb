// src/environments/environment.ts

import { Environment } from './environment.d'; // 💥 Importa a interface

export const environment: Environment = { // 💥 Aplica a interface
  production: false,
  // IMPORTANTE: Este IP (10.0.2.2) é o padrão para o Android Emulator se comunicar com o localhost da sua máquina.
  // Se estiver usando um dispositivo físico na mesma rede, substitua pelo IP da sua máquina (ex: http://192.168.1.10:8000/api/).
  // Detecta automaticamente quando estiver rodando no navegador local e usa localhost.
  apiUrl: ((): string => {
    try {
      const host = (typeof window !== 'undefined' && window.location && window.location.hostname) ? window.location.hostname : '';
      if (host === 'localhost' || host === '127.0.0.1') {
        return 'http://localhost:8000/api/';
      }
    } catch (e) {
      // fallback
    }
    return 'http://10.0.2.2:8000/api/';
  })(),
};