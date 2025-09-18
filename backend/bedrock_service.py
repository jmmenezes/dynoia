import boto3
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BedrockService:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        logger.info(f"BedrockService inicializado com modelo: {self.model_id}")
    
    def _invoke_model(self, prompt: str) -> str:
        logger.info(f"Enviando prompt para LLM: {prompt[:100]}...")
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            response_text = result['content'][0]['text']
            logger.info(f"Resposta da LLM recebida: {response_text[:100]}...")
            return response_text
            
        except Exception as e:
            logger.error(f"Erro ao invocar modelo: {str(e)}")
            raise
    
    def obter_dados_veiculo(self, nome_veiculo: str) -> Dict[str, Any]:
        logger.info(f"Obtendo dados do veículo: {nome_veiculo}")
        
        prompt = f"""
        Forneça as especificações técnicas do veículo {nome_veiculo} no formato JSON:
        {{
            "potencia_original": número em CV,
            "peso": número em kg,
            "aceleracao_0_100": número em segundos,
            "tem_turbo": true/false
        }}
        
        Responda apenas com o JSON, sem texto adicional.
        """
        
        try:
            response = self._invoke_model(prompt)
            logger.info(f"Resposta bruta da LLM: {response}")
            
            # Tentar extrair JSON da resposta
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean.replace('```json', '').replace('```', '').strip()
            
            dados = json.loads(response_clean)
            logger.info(f"Dados parseados: {dados}")
            return dados
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {str(e)}, resposta: {response}")
            raise
        except Exception as e:
            logger.error(f"Erro ao obter dados do veículo {nome_veiculo}: {str(e)}")
            raise
    
    def calcular_preparacoes(self, veiculo_data: Dict[str, Any]) -> list:
        logger.info(f"Calculando preparações para: {veiculo_data}")
        
        tem_turbo = veiculo_data['tem_turbo']
        potencia = veiculo_data['potencia_original']
        aceleracao = veiculo_data['aceleracao_0_100']
        
        if tem_turbo:
            prompt = f"""
            Calcule as preparações para um veículo turbo com {potencia}CV e aceleração 0-100 de {aceleracao}s:
            
            Cenário 1: Aumento de 50% na pressão do turbo
            Cenário 2: Aumento de 100% na pressão do turbo
            
            Responda no formato JSON:
            [
                {{"cenario": "Turbo +50%", "potencia_estimada": número, "aceleracao_estimada": número}},
                {{"cenario": "Turbo +100%", "potencia_estimada": número, "aceleracao_estimada": número}}
            ]
            """
        else:
            prompt = f"""
            Calcule as preparações para um veículo aspirado com {potencia}CV e aceleração 0-100 de {aceleracao}s:
            
            Cenário 1: Adição de turbo com 1kg de pressão
            Cenário 2: Adição de turbo com 2kg de pressão
            
            Responda no formato JSON:
            [
                {{"cenario": "Turbo 1kg", "potencia_estimada": número, "aceleracao_estimada": número}},
                {{"cenario": "Turbo 2kg", "potencia_estimada": número, "aceleracao_estimada": número}}
            ]
            """
        
        try:
            response = self._invoke_model(prompt)
            logger.info(f"Resposta preparações: {response}")
            
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean.replace('```json', '').replace('```', '').strip()
            
            preparacoes = json.loads(response_clean)
            logger.info(f"Preparações parseadas: {preparacoes}")
            return preparacoes
            
        except Exception as e:
            logger.error(f"Erro ao calcular preparações: {str(e)}")
            raise
    
    def simular_corrida(self, veiculo1: Dict[str, Any], veiculo2: Dict[str, Any]) -> str:
        logger.info(f"Simulando corrida entre {veiculo1.get('nome', 'V1')} e {veiculo2.get('nome', 'V2')}")
        
        prompt = f"""
        Simule uma corrida de 500 metros entre:
        
        Veículo 1: {veiculo1['nome']} - {veiculo1['potencia_original']}CV, 0-100 em {veiculo1['aceleracao_0_100']}s
        Veículo 2: {veiculo2['nome']} - {veiculo2['potencia_original']}CV, 0-100 em {veiculo2['aceleracao_0_100']}s
        
        Crie uma narrativa envolvente da corrida considerando as características de cada veículo.
        Máximo 300 palavras.
        """
        
        try:
            simulacao = self._invoke_model(prompt)
            logger.info(f"Simulação gerada: {simulacao[:100]}...")
            return simulacao
            
        except Exception as e:
            logger.error(f"Erro ao simular corrida: {str(e)}")
            raise
