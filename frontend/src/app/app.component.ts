import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';
import { VeiculoRequest, ComparacaoResponse, Veiculo } from './models/veiculo.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container">
      <h1>DynoIA - Comparador de Veículos</h1>
      
      <div class="card">
        <h2>Insira os dados dos veículos</h2>
        <form (ngSubmit)="compararVeiculos()" #form="ngForm">
          <div class="input-group">
            <label for="veiculo1">Veículo 1:</label>
            <input 
              type="text" 
              id="veiculo1" 
              [(ngModel)]="request.veiculo1" 
              name="veiculo1" 
              placeholder="Ex: Honda Civic Type R"
              required>
          </div>
          
          <div class="input-group">
            <label for="veiculo2">Veículo 2:</label>
            <input 
              type="text" 
              id="veiculo2" 
              [(ngModel)]="request.veiculo2" 
              name="veiculo2" 
              placeholder="Ex: Volkswagen Golf GTI"
              required>
          </div>
          
          <button type="submit" class="btn" [disabled]="loading || !form.valid">
            {{ loading ? 'Processando...' : 'Comparar Veículos' }}
          </button>
        </form>
      </div>

      <div *ngIf="loading" class="loading">
        <p>Consultando dados dos veículos e calculando preparações...</p>
      </div>

      <div *ngIf="error" class="error">
        {{ error }}
      </div>

      <div *ngIf="resultado">
        <!-- Dados dos Veículos -->
        <div class="card">
          <h2>Especificações Técnicas</h2>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
              <h3>{{ resultado.veiculo1.nome }}</h3>
              <p><strong>Potência:</strong> {{ resultado.veiculo1.potencia_original }} CV</p>
              <p><strong>Peso:</strong> {{ resultado.veiculo1.peso }} kg</p>
              <p><strong>0-100 km/h:</strong> {{ resultado.veiculo1.aceleracao_0_100 }}s</p>
              <p><strong>Turbo:</strong> {{ resultado.veiculo1.tem_turbo ? 'Sim' : 'Não' }}</p>
            </div>
            <div>
              <h3>{{ resultado.veiculo2.nome }}</h3>
              <p><strong>Potência:</strong> {{ resultado.veiculo2.potencia_original }} CV</p>
              <p><strong>Peso:</strong> {{ resultado.veiculo2.peso }} kg</p>
              <p><strong>0-100 km/h:</strong> {{ resultado.veiculo2.aceleracao_0_100 }}s</p>
              <p><strong>Turbo:</strong> {{ resultado.veiculo2.tem_turbo ? 'Sim' : 'Não' }}</p>
            </div>
          </div>
        </div>

        <!-- Preparações -->
        <div class="card">
          <h2>Cenários de Preparação</h2>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
              <h3>{{ resultado.veiculo1.nome }}</h3>
              <div *ngFor="let prep of resultado.veiculo1.preparacoes" style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <h4>{{ prep.cenario }}</h4>
                <p><strong>Potência:</strong> {{ prep.potencia_estimada }} CV</p>
                <p><strong>0-100 km/h:</strong> {{ prep.aceleracao_estimada }}s</p>
              </div>
            </div>
            <div>
              <h3>{{ resultado.veiculo2.nome }}</h3>
              <div *ngFor="let prep of resultado.veiculo2.preparacoes" style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <h4>{{ prep.cenario }}</h4>
                <p><strong>Potência:</strong> {{ prep.potencia_estimada }} CV</p>
                <p><strong>0-100 km/h:</strong> {{ prep.aceleracao_estimada }}s</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Gráfico Simples -->
        <div class="card">
          <h2>Comparação Visual</h2>
          <div class="chart-container">
            <h3>Potência (CV)</h3>
            <div class="bar-chart">
              <div class="bar-group">
                <label>{{ resultado.veiculo1.nome }}</label>
                <div class="bar" [style.width.%]="getBarWidth(resultado.veiculo1.potencia_original, maxPotencia)">
                  {{ resultado.veiculo1.potencia_original }} CV
                </div>
              </div>
              <div class="bar-group">
                <label>{{ resultado.veiculo2.nome }}</label>
                <div class="bar" [style.width.%]="getBarWidth(resultado.veiculo2.potencia_original, maxPotencia)">
                  {{ resultado.veiculo2.potencia_original }} CV
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Simulação de Corrida -->
        <div class="card">
          <h2>Simulação de Corrida - 500 metros</h2>
          <div style="white-space: pre-line; line-height: 1.6;">
            {{ resultado.simulacao_corrida }}
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    h1 {
      text-align: center;
      color: white;
      margin-bottom: 30px;
      font-size: 2.5em;
    }

    h2 {
      color: #333;
      margin-bottom: 20px;
    }

    h3 {
      color: #667eea;
      margin-bottom: 10px;
    }

    .chart-container {
      margin: 20px 0;
    }

    .bar-chart {
      margin: 20px 0;
    }

    .bar-group {
      margin: 15px 0;
    }

    .bar-group label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }

    .bar {
      background: linear-gradient(90deg, #667eea, #764ba2);
      color: white;
      padding: 10px;
      border-radius: 5px;
      text-align: center;
      font-weight: bold;
      min-width: 100px;
    }
  `]
})
export class AppComponent {
  request: VeiculoRequest = {
    veiculo1: '',
    veiculo2: ''
  };
  
  resultado: ComparacaoResponse | null = null;
  loading = false;
  error = '';
  maxPotencia = 0;

  constructor(private apiService: ApiService) {}

  compararVeiculos() {
    this.loading = true;
    this.error = '';
    this.resultado = null;

    this.apiService.compararVeiculos(this.request).subscribe({
      next: (response) => {
        this.resultado = response;
        this.maxPotencia = Math.max(
          response.veiculo1.potencia_original,
          response.veiculo2.potencia_original,
          ...response.veiculo1.preparacoes.map(p => p.potencia_estimada),
          ...response.veiculo2.preparacoes.map(p => p.potencia_estimada)
        );
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erro ao processar a comparação. Tente novamente.';
        this.loading = false;
        console.error(err);
      }
    });
  }

  getBarWidth(value: number, max: number): number {
    return (value / max) * 100;
  }
}
