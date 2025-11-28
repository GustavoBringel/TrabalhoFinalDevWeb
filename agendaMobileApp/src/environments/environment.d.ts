// src/environments/environment.d.ts

/**
 * Interface que define o formato do objeto environment.
 * Isso resolve o erro 'Property 'apiUrl' does not exist' no TypeScript.
 */
export interface Environment {
  production: boolean;
  
  // 💥 NOVO: Define que 'apiUrl' é uma string e é obrigatória
  apiUrl: string; 
}