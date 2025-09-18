# DynoIA - Comparador de Veículos com IA

Aplicação web para comparação de performance de veículos com simulação de preparações utilizando AWS Bedrock.

## Estrutura do Projeto

```
dynoia/
├── backend/           # API FastAPI (Python 3.7)
├── frontend/          # Interface Angular 19
├── run_backend.sh     # Script para executar backend
├── run_frontend.sh    # Script para executar frontend
└── README.md
```

## Pré-requisitos

### Backend
- Python 3.7+
- Credenciais AWS configuradas
- Acesso ao AWS Bedrock (região us-east-1)

### Frontend
- Node.js 18+
- npm ou yarn

## Configuração AWS

1. Configure suas credenciais AWS:
```bash
aws configure
```

2. Certifique-se de ter acesso ao AWS Bedrock na região us-east-1

3. O modelo utilizado é: `anthropic.claude-3-sonnet-20240229-v1:0`

## Instalação e Execução

### Backend

```bash
# Tornar o script executável
chmod +x run_backend.sh

# Executar backend
./run_backend.sh
```

O backend estará disponível em: http://localhost:8000

### Frontend

```bash
# Tornar o script executável
chmod +x run_frontend.sh

# Executar frontend
./run_frontend.sh
```

O frontend estará disponível em: http://localhost:4200

## Como Usar

1. Acesse http://localhost:4200
2. Insira os nomes de 2 veículos nos campos
3. Clique em "Comparar Veículos"
4. Aguarde o processamento (pode levar até 30 segundos)
5. Visualize:
   - Especificações técnicas originais
   - Cenários de preparação calculados
   - Gráfico comparativo de potência
   - Simulação de corrida de 500 metros

## Funcionalidades

- **Consulta de dados técnicos**: Potência, peso, aceleração 0-100km/h
- **Cálculos de preparação**:
  - Veículos aspirados: Turbo com 1kg e 2kg de pressão
  - Veículos turbo: Aumento de 50% e 100% na pressão
- **Visualização comparativa**: Gráficos de potência
- **Simulação de corrida**: Narrativa gerada por IA

## API Endpoints

### POST /api/comparar-veiculos
Compara dois veículos e retorna dados técnicos, preparações e simulação.

**Request:**
```json
{
  "veiculo1": "Honda Civic Type R",
  "veiculo2": "Volkswagen Golf GTI"
}
```

**Response:**
```json
{
  "veiculo1": {
    "nome": "Honda Civic Type R",
    "potencia_original": 320,
    "peso": 1380,
    "aceleracao_0_100": 5.7,
    "tem_turbo": true,
    "preparacoes": [...]
  },
  "veiculo2": {...},
  "simulacao_corrida": "Texto da simulação...",
  "status": "success",
  "mensagem": "Comparação realizada com sucesso"
}
```

### GET /health
Verifica se a API está funcionando.

## Troubleshooting

### Erro de credenciais AWS
- Verifique se as credenciais estão configuradas: `aws configure list`
- Certifique-se de ter permissões para o Bedrock

### Erro de modelo não encontrado
- Verifique se o modelo Claude 3 Sonnet está disponível na sua região
- Solicite acesso ao modelo no console AWS Bedrock

### Timeout na API
- As consultas à LLM podem demorar até 30 segundos
- Verifique a conectividade com a AWS

## Desenvolvimento

### Estrutura do Backend
- `main.py`: API principal FastAPI
- `models.py`: Modelos Pydantic
- `bedrock_service.py`: Integração com AWS Bedrock

### Estrutura do Frontend
- `app.component.ts`: Componente principal
- `api.service.ts`: Serviço para comunicação com API
- `veiculo.model.ts`: Interfaces TypeScript

## Custos AWS

O uso do AWS Bedrock gera custos baseados no número de tokens processados. Monitore o uso no console AWS para controlar os gastos.

## Lista de prompts

gere uma aplicação web responsiva com frontend em angular 19 e backend em python 3.7 que irá se comunicar com o LLM da aws bedrock. 
o usuário deve fornecer 2 veículos 
a llm deverá obter o peso e potência dos veículos e exibir na tela
então a llm deve calcular uma potência estimada para carros aspirados usando turbo com 1kg e 2kg e carros turbo com aumebto de pressão em 50% e 100%
então deve ser gerada uma simulação de uma corrida entre os carros em um percurso de 500 metros

