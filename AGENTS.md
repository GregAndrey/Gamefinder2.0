# AGENTS.md: Agente GameFinder

## Goal

Construir o **`agente-gamefinder`**: um agente **Google ADK** (Python) movido a skills, que atua como consultor e motor de recomendação inteligente de jogos para PC (Steam), PlayStation e Xbox a partir da skill `skills/game-finder/`. O agente traduz as preferências do jogador (plataformas ativas, gêneros, ambientações, estilo de gameplay e histórico de jogos amados/não curtidos) em recomendações precisas com cálculo de afinidade (match %) e justificativas transparentes ("Por que recomendamos"). Além disso, o agente gerencia a lista de desejos e recomendações, salvando a agenda/wishlist em arquivo CSV com o **EnvironmentToolset** do ADK e rodando localmente no **ADK Web**.

## Context

* **Quem é você:** um engenheiro de software especialista em IA, fazendo pair programming com quem está desenvolvendo o agente. Explique **o que** está fazendo e **por quê**, em português do Brasil, de forma curta e objetiva.
* **Ambiente:** Google Cloud Shell ou máquina local. O `agy` roda na raiz do repositório, e o projeto do agente fica em `./agente-gamefinder/`, criado com as convenções do **agents-cli**.
* **Skills do ADK** ([adk.dev/skills](https://adk.dev/skills/)): carregadas com `load_skill_from_dir` e expostas pelo `SkillToolset`, que dá ao agente as ferramentas `load_skill` e `load_skill_resource`. A skill usa divulgação progressiva:
  * **L1:** `name` e `description` no frontmatter do `SKILL.md`.
  * **L2:** o corpo do `SKILL.md`, com a regra de gating de preferências e perfil.
  * **L3:** `references/workflow.md`, `references/algoritmo_afinidade.md`, `references/catalogo_jogos.md`, `references/salvar_dados.md`, `assets/recomendacao_template.md` e `assets/exemplo_recomendacao.md`.
* **EnvironmentToolset** ([adk.dev/integrations/environment-toolset](https://adk.dev/integrations/environment-toolset/)): dá ao agente ferramentas de arquivo (`ReadFile`, `WriteFile`, `EditFile`) e de shell (`Execute`) dentro de um `LocalEnvironment`. O agente usa `WriteFile` para gravar `wishlist.csv` (ou `recomendacoes.csv`) e `ReadFile` para conferir a lista salva antes de reescrever em caso de refinamento ou descarte de títulos. É um recurso experimental (ADK Python ≥ 1.29) e emite `UserWarning` ao iniciar, o que é esperado.
* **Regra de gating da skill:** sem **plataformas ativas** (Steam, PlayStation e/ou Xbox), **gêneros e ambientações favoritas**, **estilo de gameplay/ritmo** e **histórico de jogos conhecidos** (o que já jogou e amou vs. o que detestou), o agente pergunta só o que falta e não carrega nenhum recurso L3. Com tudo em mãos, ele segue o `workflow.md` até entregar a curadoria no formato do `recomendacao_template.md` e salvar a lista com `WriteFile`.
* **Autenticação local:** API Key do Google AI Studio no arquivo `agente-gamefinder/.env`:
  ```env
  GOOGLE_GENAI_USE_VERTEXAI=FALSE
  GEMINI_API_KEY=<sua-api-key>
  MODEL=gemini-3.8-flash
  ```
* **Execução local:**
  ```bash
  cd agente-gamefinder
  uv run adk web --allow_origins="*"   # libera o proxy do Web Preview do Cloud Shell
  ```

## Constraints

* **Framework:** use só o **Google ADK** em Python, seguindo a especificação de ADK Skills (`load_skill_from_dir` + `SkillToolset`).
* **Divulgação progressiva:** **não** cole o conteúdo de `references/` ou `assets/` na instrução do agente. O conteúdo deve ser carregado sob demanda pelas ferramentas da skill.
* **Empacotamento da skill:** copie `skills/game-finder/` para `agente-gamefinder/app/skills/game-finder/`, porque o ADK resolve o caminho a partir do `agent.py`. A pasta precisa ter **exatamente** o nome do campo `name` do frontmatter. Ao alterar uma skill, mantenha as duas cópias sincronizadas.
* **Ferramentas de arquivo:** use `EnvironmentToolset(environment=LocalEnvironment(working_dir=...))`, com `working_dir` apontando para `agente-gamefinder/dados/` (caminho absoluto calculado a partir do `agent.py`). Sem `working_dir`, o ADK usa uma pasta temporária que é apagada quando o agente encerra.
* **Sem shell:** exponha só `ReadFile` e `WriteFile`. O agente não precisa executar comandos. No ADK 2.x, o `tool_filter` **não** é aplicado pelo `EnvironmentToolset`, então filtre com uma subclasse que sobrescreve `get_tools`:
  ```python
  class FerramentasDeArquivo(EnvironmentToolset):
      async def get_tools(self, readonly_context=None):
          tools = await super().get_tools(readonly_context)
          return [t for t in tools if t.name in ("ReadFile", "WriteFile")]
  ```
* **Filtro rígido de plataforma:** se o usuário não possuir determinada plataforma, nenhum jogo exclusivo dessa plataforma ausente pode ser recomendado.
* **Transparência do Match:** cada recomendação deve vir acompanhada da porcentagem de afinidade e da justificativa explícita ("Por que recomendamos").
* **Modelo:** leia o modelo da variável de ambiente `MODEL`, com padrão `gemini-3.8-flash`. Não deixe o nome do modelo fixo no código.
* **Data atual:** injete a data de hoje na instrução do agente, via *instruction provider* do ADK, para situar lançamentos recentes e atualizações de catálogo.
* **Segredos:** **nunca** versione o `.env` nem a pasta `dados/` (ela guarda preferências e listas do usuário) nem escreva a API Key em código, README, testes ou logs.
* **Dependências:** gerencie com `uv` dentro de `agente-gamefinder/` (`uv sync`).
* **Simplicidade:** prefira código simples e legível a abstrações sofisticadas. Confirme o entendimento do pedido antes de gerar muito código.
* **Fora de escopo:** deploy no Agent Runtime, Gemini Enterprise e infraestrutura de nuvem pesada. Não gere esses artefatos, a menos que isso seja pedido explicitamente.

## Done-when

- [ ] `agente-gamefinder/app/agent.py` define um `root_agent` com o `SkillToolset` carregando `app/skills/game-finder` e o `EnvironmentToolset` expondo só `ReadFile` e `WriteFile`.
- [ ] O modelo vem da variável `MODEL`, e a instrução do agente contém a data de hoje.
- [ ] `uv sync` e `uv run adk web --allow_origins="*"` rodam sem erros, e o agente `app` aparece no ADK Web.
- [ ] **Gating:** com uma mensagem vaga como "Quero achar um jogo bom para jogar hoje", o agente pede só as informações que faltam (plataformas, gêneros/ambientação, ritmo/tempo e histórico) e **não** chama `load_skill_resource`.
- [ ] **Recomendação completa:** com todas as informações (ex.: PC/Steam, RPG com foco em história e fantasia medieval, amou The Witcher 3), o agente carrega `workflow.md`, `catalogo_jogos.md`, `algoritmo_afinidade.md`, `recomendacao_template.md` e `salvar_dados.md`, entrega as recomendações com % de afinidade e justificativa, e chama `WriteFile`, criando `agente-gamefinder/dados/wishlist.csv` com um CSV válido de lista de desejos.
- [ ] **Filtro de plataforma respeitado:** se o usuário selecionou apenas PlayStation, nenhum exclusivo de PC ou Xbox é sugerido.
- [ ] **Refinamento/Descarte:** quando o usuário rejeita uma sugestão ("Não curti a ideia desse jogo"), o agente recalibra a recomendação, substitui por um título alternativo e sobrescreve o `wishlist.csv` mantendo o histórico consistente.
- [ ] Nenhum `.env`, API Key ou arquivo da pasta `dados/` aparece em arquivos versionados do git.
