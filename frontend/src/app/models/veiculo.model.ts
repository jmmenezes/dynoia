export interface VeiculoRequest {
  veiculo1: string;
  veiculo2: string;
}

export interface Preparacao {
  cenario: string;
  potencia_estimada: number;
  aceleracao_estimada: number;
}

export interface Veiculo {
  nome: string;
  potencia_original: number;
  peso: number;
  aceleracao_0_100: number;
  tem_turbo: boolean;
  preparacoes: Preparacao[];
}

export interface ComparacaoResponse {
  veiculo1: Veiculo;
  veiculo2: Veiculo;
  simulacao_corrida: string;
  status: string;
  mensagem: string;
}
