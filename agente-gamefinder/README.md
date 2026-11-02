# Agente GameFinder

Agente especialista em recomendação e curadoria inteligente de jogos para Steam, PlayStation e Xbox, construído com o **Google ADK** (Agent Development Kit) e movido a skills.

## Requisitos

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) instalado
- Chave de API do Google AI Studio configurada no arquivo `.env`

## Configuração

1. Crie o arquivo `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

2. Insira sua chave do Google AI Studio:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GEMINI_API_KEY=sua-api-key-aqui
MODEL=gemini-3.8-flash
```

3. Sincronize as dependências com `uv`:

```bash
uv sync
```

## Execução

Inicie o servidor local do ADK Web:

```bash
uv run adk web --allow_origins="*"
```

Abra a interface web indicada no terminal e selecione o agente `app`.
