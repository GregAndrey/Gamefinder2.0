"""Agente GameFinder: Hub de Recomendação de Jogos com Google ADK."""

import os
from datetime import date
from pathlib import Path

from google.adk.agents import Agent
from google.adk.skills import SkillToolset, load_skill_from_dir
from google.adk.tools.environment import EnvironmentToolset, LocalEnvironment


class FerramentasDeArquivo(EnvironmentToolset):
    """Subclasse que expõe estritamente ReadFile e WriteFile para o agente."""

    async def get_tools(self, readonly_context=None):
        tools = await super().get_tools(readonly_context)
        return [t for t in tools if t.name in ("ReadFile", "WriteFile")]


# Resolução de caminhos absolutos
BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = (BASE_DIR.parent / "dados").resolve()
DADOS_DIR.mkdir(parents=True, exist_ok=True)

SKILL_PATH = (BASE_DIR / "skills" / "game-finder").resolve()


def dynamic_instructions() -> str:
    """Provedor de instruções dinâmicas com injeção da data atual."""
    hoje = date.today().strftime("%d/%m/%Y")
    return (
        f"Você é o GameFinder, um consultor gamer especialista e hub inteligente de recomendação "
        f"de jogos para Steam, PlayStation e Xbox.\n"
        f"A data atual é {hoje}.\n\n"
        f"Sua missão é entender o perfil do jogador, aplicar o filtro estrito de plataformas que ele possui, "
        f"calcular a afinidade (match %) com base em gêneros, ritmo de jogo e títulos amados/odiados, "
        f"apresentar justificativas transparentes ('Por que recomendamos') e salvar a lista de desejos "
        f"e recomendações no arquivo 'wishlist.csv'.\n\n"
        f"Você opera através de skills e ferramentas de arquivo. Siga estritamente as regras de ativação "
        f"(gating) e o fluxo da skill game-finder antes de carregar recursos aprofundados."
    )


# Modelo configurável via variável de ambiente MODEL
MODEL_NAME = os.getenv("MODEL", "gemini-3.8-flash")

# Agente raiz do Google ADK
root_agent = Agent(
    name="app",
    model=MODEL_NAME,
    instructions=dynamic_instructions,
    toolsets=[
        SkillToolset(skills=[load_skill_from_dir(SKILL_PATH)]),
        FerramentasDeArquivo(environment=LocalEnvironment(working_dir=str(DADOS_DIR))),
    ],
)
