import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { VeiculoRequest, ComparacaoResponse } from '../models/veiculo.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  compararVeiculos(request: VeiculoRequest): Observable<ComparacaoResponse> {
    return this.http.post<ComparacaoResponse>(`${this.baseUrl}/comparar-veiculos`, request);
  }
}
