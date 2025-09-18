# Documento de Requisitos - DynoIA

## 1. Visão Geral do Projeto

### 1.1 Nome do Projeto
DynoIA

### 1.2 Descrição
Aplicação web para comparação de performance de veículos com simulação de preparações utilizando IA generativa.

### 1.3 Objetivo
Permitir aos usuários comparar dois veículos e visualizar estimativas de performance em diferentes cenários de preparação, incluindo simulação de corrida.

## 2. Arquitetura Técnica

### 2.1 Frontend
- **Framework**: Angular 19
- **Linguagem**: TypeScript
- **Responsabilidades**: Interface do usuário, entrada de dados, exibição de resultados e gráficos

### 2.2 Backend
- **Framework**: FastAPI
- **Linguagem**: Python 3.7
- **Responsabilidades**: API REST, integração com AWS Bedrock, processamento de dados

### 2.3 Serviços Externos
- **AWS Bedrock**: LLM para obtenção de dados técnicos e cálculos de performance

## 3. Requisitos Funcionais

### 3.1 RF001 - Entrada de Dados de Veículos
- **Descrição**: O sistema deve permitir a entrada de dados de 2 veículos
- **Critérios de Aceitação**:
  - Interface com 2 campos para identificação dos veículos
  - Validação de entrada obrigatória
  - Envio dos dados para o backend via API

### 3.2 RF002 - Obtenção de Dados Técnicos
- **Descrição**: O sistema deve obter dados técnicos dos veículos via AWS Bedrock
- **Critérios de Aceitação**:
  - Consultar LLM para obter: potência, peso, aceleração 0-100km/h
  - Identificar se o veículo possui turbo ou é aspirado
  - Retornar dados estruturados

### 3.3 RF003 - Cálculo de Preparações
- **Descrição**: O sistema deve calcular estimativas de performance para 2 cenários de preparação
- **Critérios de Aceitação**:
  - **Veículos Aspirados**:
    - Cenário 1: Adição de turbo com 1kg de pressão
    - Cenário 2: Adição de turbo com 2kg de pressão
  - **Veículos Turbo**:
    - Cenário 1: Aumento de 50% na pressão atual
    - Cenário 2: Aumento de 100% na pressão atual
  - Calcular potência e aceleração estimadas para cada cenário

### 3.4 RF004 - Geração de Gráficos Comparativos
- **Descrição**: O sistema deve gerar gráficos comparando os 2 veículos nos 3 cenários
- **Critérios de Aceitação**:
  - Gráfico de potência (original vs preparações)
  - Gráfico de aceleração 0-100km/h (original vs preparações)
  - Comparação visual entre os 2 veículos
  - Interface responsiva para visualização

### 3.5 RF005 - Simulação de Corrida
- **Descrição**: O sistema deve gerar uma narrativa de corrida entre os 2 veículos
- **Critérios de Aceitação**:
  - Percurso de 500 metros
  - Texto gerado pela LLM simulando a corrida
  - Considerar as características de cada veículo nos diferentes cenários
  - Apresentação em formato legível e envolvente

## 4. Requisitos Não-Funcionais

### 4.1 RNF001 - Performance
- Tempo de resposta da API: máximo 30 segundos
- Carregamento da interface: máximo 3 segundos

### 4.2 RNF002 - Usabilidade
- Interface intuitiva e responsiva
- Compatibilidade com navegadores modernos (Chrome, Firefox, Safari, Edge)

### 4.3 RNF003 - Segurança
- Validação de entrada no frontend e backend
- Tratamento seguro de credenciais AWS
- Rate limiting para chamadas à API

### 4.4 RNF004 - Confiabilidade
- Tratamento de erros da AWS Bedrock
- Fallback para casos de indisponibilidade do serviço
- Logs de auditoria das operações

## 5. Casos de Uso

### 5.1 UC001 - Comparar Veículos
**Ator**: Usuário
**Pré-condições**: Aplicação carregada
**Fluxo Principal**:
1. Usuário insere dados do primeiro veículo
2. Usuário insere dados do segundo veículo
3. Sistema valida os dados
4. Sistema consulta AWS Bedrock para obter especificações técnicas
5. Sistema calcula cenários de preparação
6. Sistema exibe gráficos comparativos
7. Sistema gera e exibe simulação de corrida

**Fluxos Alternativos**:
- FA001: Veículo não encontrado na base da LLM
- FA002: Erro na comunicação com AWS Bedrock
- FA003: Dados insuficientes para cálculos

## 6. Estrutura de Dados

### 6.1 Modelo de Veículo
```json
{
  "nome": "string",
  "potencia_original": "number",
  "peso": "number",
  "aceleracao_0_100": "number",
  "tem_turbo": "boolean",
  "preparacoes": [
    {
      "cenario": "string",
      "potencia_estimada": "number",
      "aceleracao_estimada": "number"
    }
  ]
}
```

### 6.2 Modelo de Comparação
```json
{
  "veiculo1": "Veiculo",
  "veiculo2": "Veiculo",
  "graficos": {
    "potencia": "ChartData",
    "aceleracao": "ChartData"
  },
  "simulacao_corrida": "string"
}
```

## 7. APIs

### 7.1 POST /api/comparar-veiculos
**Entrada**:
```json
{
  "veiculo1": "string",
  "veiculo2": "string"
}
```

**Saída**:
```json
{
  "comparacao": "Comparacao",
  "status": "success|error",
  "mensagem": "string"
}
```

## 8. Integração com AWS Bedrock

### 8.1 Prompts para LLM
1. **Obtenção de dados técnicos**: Consulta especificações do veículo
2. **Cálculo de preparações**: Estimativa de ganhos de performance
3. **Simulação de corrida**: Geração de narrativa comparativa

### 8.2 Configuração
- Modelo recomendado: Claude 3 ou similar
- Região AWS: us-east-1 (ou conforme disponibilidade)
- Configuração de timeout: 25 segundos

## 9. Cronograma Estimado

### Fase 1 - Setup e Backend (1-2 semanas)
- Configuração do ambiente FastAPI
- Integração com AWS Bedrock
- Desenvolvimento das APIs básicas

### Fase 2 - Frontend (1-2 semanas)
- Setup Angular 19
- Desenvolvimento da interface
- Integração com backend

### Fase 3 - Funcionalidades Avançadas (1 semana)
- Implementação de gráficos
- Refinamento da simulação de corrida
- Testes e ajustes

### Fase 4 - Testes e Deploy (1 semana)
- Testes integrados
- Otimizações de performance
- Deploy e documentação

## 10. Riscos e Mitigações

### 10.1 Limitações da LLM
- **Risco**: Dados imprecisos ou inconsistentes
- **Mitigação**: Validação cruzada e fallbacks

### 10.2 Custos AWS Bedrock
- **Risco**: Custos elevados com muitas consultas
- **Mitigação**: Cache de resultados e rate limiting

### 10.3 Performance
- **Risco**: Tempo de resposta elevado
- **Mitigação**: Processamento assíncrono e indicadores de progresso

## 11. Critérios de Aceitação do Projeto

- [ ] Interface funcional para entrada de 2 veículos
- [ ] Integração completa com AWS Bedrock
- [ ] Cálculos de preparação implementados
- [ ] Gráficos comparativos funcionais
- [ ] Simulação de corrida gerando texto coerente
- [ ] Tratamento de erros implementado
- [ ] Documentação técnica completa
- [ ] Testes básicos implementados
