from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import VeiculoRequest, ComparacaoResponse, Veiculo, Preparacao
from bedrock_service import BedrockService
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="DynoIA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bedrock_service = BedrockService()

@app.post("/api/comparar-veiculos", response_model=ComparacaoResponse)
async def comparar_veiculos(request: VeiculoRequest):
    logger.info(f"Recebida requisição: {request}")
    
    try:
        # Obter dados do primeiro veículo
        logger.info(f"Obtendo dados do veículo 1: {request.veiculo1}")
        dados_v1 = bedrock_service.obter_dados_veiculo(request.veiculo1)
        logger.info(f"Dados veículo 1 obtidos: {dados_v1}")
        
        logger.info(f"Calculando preparações do veículo 1")
        preparacoes_v1 = bedrock_service.calcular_preparacoes(dados_v1)
        logger.info(f"Preparações veículo 1: {preparacoes_v1}")
        
        # Adicionar nome aos dados do veículo 1
        dados_v1['nome'] = request.veiculo1
        
        veiculo1 = Veiculo(
            nome=request.veiculo1,
            potencia_original=dados_v1['potencia_original'],
            peso=dados_v1['peso'],
            aceleracao_0_100=dados_v1['aceleracao_0_100'],
            tem_turbo=dados_v1['tem_turbo'],
            preparacoes=[Preparacao(**prep) for prep in preparacoes_v1]
        )
        logger.info(f"Objeto veículo 1 criado: {veiculo1}")
        
        # Obter dados do segundo veículo
        logger.info(f"Obtendo dados do veículo 2: {request.veiculo2}")
        dados_v2 = bedrock_service.obter_dados_veiculo(request.veiculo2)
        logger.info(f"Dados veículo 2 obtidos: {dados_v2}")
        
        logger.info(f"Calculando preparações do veículo 2")
        preparacoes_v2 = bedrock_service.calcular_preparacoes(dados_v2)
        logger.info(f"Preparações veículo 2: {preparacoes_v2}")
        
        # Adicionar nome aos dados do veículo 2
        dados_v2['nome'] = request.veiculo2
        
        veiculo2 = Veiculo(
            nome=request.veiculo2,
            potencia_original=dados_v2['potencia_original'],
            peso=dados_v2['peso'],
            aceleracao_0_100=dados_v2['aceleracao_0_100'],
            tem_turbo=dados_v2['tem_turbo'],
            preparacoes=[Preparacao(**prep) for prep in preparacoes_v2]
        )
        logger.info(f"Objeto veículo 2 criado: {veiculo2}")
        
        # Simular corrida
        logger.info("Iniciando simulação de corrida")
        simulacao = bedrock_service.simular_corrida(dados_v1, dados_v2)
        logger.info(f"Simulação concluída: {simulacao[:100]}...")
        
        response = ComparacaoResponse(
            veiculo1=veiculo1,
            veiculo2=veiculo2,
            simulacao_corrida=simulacao,
            status="success",
            mensagem="Comparação realizada com sucesso"
        )
        
        logger.info("Comparação concluída com sucesso")
        return response
        
    except Exception as e:
        logger.error(f"Erro na comparação: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/health")
async def health_check():
    logger.info("Health check solicitado")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor DynoIA")
    uvicorn.run(app, host="0.0.0.0", port=8000)
