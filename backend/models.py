from pydantic import BaseModel
from typing import List, Optional

class VeiculoRequest(BaseModel):
    veiculo1: str
    veiculo2: str

class Preparacao(BaseModel):
    cenario: str
    potencia_estimada: float
    aceleracao_estimada: float

class Veiculo(BaseModel):
    nome: str
    potencia_original: float
    peso: float
    aceleracao_0_100: float
    tem_turbo: bool
    preparacoes: List[Preparacao]

class ComparacaoResponse(BaseModel):
    veiculo1: Veiculo
    veiculo2: Veiculo
    simulacao_corrida: str
    status: str
    mensagem: str
