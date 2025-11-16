# Agente Assistivo de Aprendizagem (SaaS Protótipo)

## Overview
Microsserviço Flask que atua como um agente de IA para fins educacionais, utilizando o ReplitDB para persistência e a API do Google Gemini para a lógica de resposta inteligente.

## Arquitetura
- **Linguagem:** Python 3.11
- **Framework Web:** Flask
- **Banco de Dados:** ReplitDB
- **IA:** Google Gemini 1.5 Flash
- **Segurança:** Chave de API em Variável de Ambiente (GEMINI_API_KEY)

## Estrutura do Projeto
```
.
├── main.py                 # Aplicação Flask principal
├── .env                    # Variáveis de ambiente (não commitado)
├── .env.example            # Exemplo de variáveis de ambiente
├── pyproject.toml          # Dependências Python
└── replit.md              # Esta documentação
```

## Endpoints da API

### GET /
Retorna o nome e versão do projeto.

**Resposta:**
```json
{
  "name": "Agente Assistivo de Aprendizagem",
  "version": "1.0.0"
}
```

### POST /api/ask
Aceita uma consulta do usuário e retorna uma resposta educacional gerada pela IA.

**Request Body:**
```json
{
  "user_id": "string",
  "topic": "string"
}
```

**Resposta:**
```json
{
  "summary": "Explicação concisa do tópico",
  "next_steps": ["passo 1", "passo 2", "passo 3"]
}
```

**Erros:**
- 400: JSON malformado, campos ausentes ou Content-Type incorreto

### GET /api/get_history?user_id=X
Retorna o histórico de consultas de um usuário ordenado cronologicamente (mais recente primeiro).

**Resposta:**
```json
{
  "history": [
    [timestamp, "topic"],
    [timestamp, "topic"]
  ]
}
```

**Erros:**
- 400: user_id ausente

## Configuração

### 1. Obter Chave da API do Gemini
1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crie uma nova chave de API
3. Adicione a chave nas variáveis de ambiente do Replit como `GEMINI_API_KEY`

### 2. Instalar Dependências
As dependências já estão instaladas via uv:
- flask
- google-generativeai
- replit
- python-dotenv

### 3. Executar o Servidor
```bash
python main.py
```

O servidor estará disponível em `http://0.0.0.0:5000`

## Persistência de Dados
O ReplitDB é usado para armazenar consultas com o seguinte formato de chave:
```
query:{user_id}:{timestamp}
```

Cada entrada contém:
```json
{
  "user_id": "string",
  "topic": "string",
  "timestamp": integer
}
```

## Funcionalidades Implementadas
- ✅ Servidor Flask com estrutura modular
- ✅ Endpoint GET / retornando nome e versão
- ✅ Endpoint POST /api/ask com validação robusta
- ✅ Integração com Google Gemini AI
- ✅ Prompt otimizado forçando JSON schema específico
- ✅ Persistência no ReplitDB
- ✅ Endpoint GET /api/get_history com ordenação reversa
- ✅ Tratamento de erros 400 para JSON malformado e campos ausentes
- ✅ Gerenciamento seguro de GEMINI_API_KEY via variáveis de ambiente

## Próximas Fases (Futuro)
- Interface web frontend para interação
- Sistema de categorização automática de tópicos
- Rate limiting por usuário
- Dashboard de analytics
- Sistema de feedback para melhorar respostas

## Data da Última Atualização
16 de novembro de 2025
