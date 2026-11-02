# 🎮 Imersão Dev Engenharia de Software na Era da IA: GameFinder com Antigravity CLI + Google ADK

Neste lab você vai usar o **Antigravity CLI (`agy`)** para criar, com o **Google ADK**, um agente especialista em recomendação e curadoria inteligente de jogos: o **GameFinder**. O agente usa a skill [`game-finder`](skills/game-finder/SKILL.md): você informa suas plataformas ativas (Steam, PlayStation, Xbox), gostos, ritmo de jogo e histórico anterior, e ele gera um feed de recomendações personalizadas com índice de afinidade (match %), justificativas transparentes e salva sua lista de desejos em um arquivo CSV usando o [EnvironmentToolset](https://adk.dev/integrations/environment-toolset/) do ADK.

## Pré-requisitos

- Conta Google com um projeto do Google Cloud com faturamento ativo (os créditos do [free trial](https://cloud.google.com/free) servem)
- Chave de API do Google AI Studio, criada em [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Conta no GitHub

---

# Aula 3: Introdução ao Antigravity CLI

## 1. Preparar o Cloud Shell

Abra o [Console do Google Cloud](https://console.cloud.google.com/), selecione o seu projeto e clique em **Ativar o Cloud Shell** (ícone `>_`). Depois rode:

```bash
export PROJECT_ID=$(gcloud config get-value project)
echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> ~/.bashrc

# Habilita a Agent Platform (acesso aos modelos usados pelo agy)
gcloud services enable aiplatform.googleapis.com cloudaicompanion.googleapis.com

git clone https://github.com/SEU_USUARIO/gamefinder.git ~/gamefinder
cd ~/gamefinder
```

> Se o Cloud Shell não abrir no projeto certo, rode `gcloud config set project SEU_PROJECT_ID` antes.

## 2. Instalar e configurar o `agy`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://antigravity.google/cli/install.sh | bash
source ~/.bashrc
```

Para iniciar o Antigravity CLI, utilize o comando:

```bash
agy
```

No setup do `agy`, escolha:

1. `Use a Google Cloud project` → `Continue with Google Cloud`
2. Abra o link, autorize com a sua conta e cole o código no terminal
3. Cole o ID do projeto (`echo $PROJECT_ID`)
4. Location: `global` · License: `Agent Platform`
5. Aceite os termos e confirme `Yes, I trust this folder`

> Dica: no Cloud Shell, use `CTRL+SHIFT+V` para colar. O `CTRL+C` encerra o programa.

## 3. Primeiros passos no `agy`

Teste alguns comandos e prompts:

```text
/help
```

```text
Leia skills/game-finder/SKILL.md e me explique o que essa skill faz.
```

Saia com `/exit`.

## 4. Instalar o agents-cli

```bash
uvx google-agents-cli setup
agy
```

No `agy`:

1. Rode `/skills` e confira se aparecem as skills `google-agents-cli-*`.
2. Rode `/config` e mude **Tool Permission** para `always-proceed`.

## 5. Criar o agente com `/grill-me`

```text
/grill-me
```

O `agy` vai te entrevistar sobre o agente. Use estas respostas como base:

- **Objetivo:** um consultor inteligente de recomendação e descoberta de jogos multiplataforma (Steam, PlayStation e Xbox), que calcula afinidade (match %), traz justificativas honestas ("Por que recomendamos") e gerencia listas de desejos e histórico de jogos.
- **Skills:** usar ADK Skills ([adk.dev/skills](https://adk.dev/skills/)) com a skill `skills/game-finder`.
- **Comportamento:** se faltar plataforma ativa, preferências de gênero/ambientação, ritmo/tempo disponível ou histórico de jogos, o agente pergunta antes de gerar as recomendações (gating).
- **Arquivos:** o agente salva a lista em `wishlist.csv` usando o [EnvironmentToolset](https://adk.dev/integrations/environment-toolset/), expondo apenas leitura e escrita, sem acesso ao shell.
- **Execução:** local, no ADK Web, com API Key do Google AI Studio. Sem deploy.

Depois peça a criação do projeto:

```text
Crie um agente ADK chamado agente-gamefinder seguindo as convenções do agents-cli e a especificação de ADK Skills. Copie a skill skills/game-finder para agente-gamefinder/app/skills/ e carregue-a com SkillToolset. Adicione o EnvironmentToolset com um LocalEnvironment na pasta agente-gamefinder/dados/, expondo só as ferramentas ReadFile e WriteFile, para o agente salvar a wishlist. O modelo vem da variável MODEL e a instrução do agente deve incluir a data de hoje. Sem configuração de deploy.
```

Saia com `/exit`.

---

# Aula 4: Engenharia de software com IA e CLI

## 6. Configurar a API Key

Configure o agente com a sua chave do AI Studio (ela não aparece na tela):

```bash
cd ~/gamefinder/agente-gamefinder
read -s -p "Cole sua API Key: " KEY && echo

cat << EOF > .env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GEMINI_API_KEY=${KEY}
MODEL=gemini-3.8-flash
EOF

uv sync
```

## 7. Testar no ADK Web

```bash
uv run adk web --allow_origins="*"
```

Clique no link `http://127.0.0.1:8000` que aparece no terminal e escolha o agente `app`. Teste:

1. **Pedido incompleto (Gating):** o agente deve fazer perguntas antes de recomendar.
    ```text
    Quero achar um jogo bom para jogar hoje.
    ```
2. **Pedido completo:** o agente deve entregar o Top Escolha, cards com afinidade (%), justificativa e chamar a ferramenta `WriteFile` para salvar `wishlist.csv`.
    ```text
    Tenho PC (Steam) e PlayStation 5. Adoro RPGs focados em história e fantasia medieval, com boa narrativa e escolhas morais. Amei The Witcher 3 e Dragon Age: Origins, mas detesto jogos com grind repetitivo ou sem história. Jogo cerca de 6h por semana.
    ```
3. **Ajuste e refinamento:** o agente deve substituir o jogo rejeitado e sobrescrever o CSV.
    ```text
    Não curti a sugestão de Lies of P porque não gosto de temas com fantoches. Pode trocar por outra indicação de ação ou RPG compatível com meu perfil?
    ```

No ADK Web, clique nos eventos `WriteFile` para ver os argumentos e a resposta da ferramenta. Depois confira o arquivo numa segunda aba do Cloud Shell:

```bash
cat ~/gamefinder/agente-gamefinder/dados/wishlist.csv
cloudshell download ~/gamefinder/agente-gamefinder/dados/wishlist.csv
```

## 8. Evoluir o agente com o `agy`

Abra uma segunda aba no Cloud Shell (`+`) e rode:

```bash
cd ~/gamefinder
agy
```

**Revisão de código:**

```text
Revise o código do agente-gamefinder e liste os problemas por severidade antes de corrigir.
```

**Validar o resultado:**

```text
Leia agente-gamefinder/dados/wishlist.csv e confira se ele segue as regras do CSV em skills/game-finder/references/salvar_dados.md: cabeçalho correto, aspas nos campos de texto e títulos compatíveis com as plataformas ativas.
```

**Corrigir um problema que você viu no teste:**

```text
No teste do ADK Web, o agente [descreva o comportamento]. Descubra a causa e corrija.
```

**Nova skill:**

```text
Crie uma skill ADK chamada quiz-o-que-jogar-hoje, no mesmo padrão da game-finder, que faz 3 perguntas rápidas (humor, tempo da sessão e formato solo/coop) para decidir 2 jogos imediatos. Adicione-a ao agente.
```

Para testar, reinicie o ADK Web na primeira aba (`CTRL+C` e `uv run adk web --allow_origins="*"`).

## 9. Versionar no GitHub

1. Configure o seu nome e e-mail no git:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

2. No `agy`, peça para preparar os commits:

```text
Confira se não há API Key em nenhum arquivo versionado e faça commits com mensagens descritivas das mudanças.
```

3. Saia do `agy` (`/exit`) e envie para o seu repositório no GitHub:

```bash
cd ~/gamefinder
git remote set-url origin https://github.com/SEU_USUARIO/gamefinder.git
git push -u origin main
```

---

## 📚 Referências

- [Antigravity CLI](https://antigravity.google/)
- [Google ADK: documentação](https://adk.dev/)
- [ADK Skills](https://adk.dev/skills/) · [Especificação Agent Skills](https://agentskills.io/specification)
- [ADK EnvironmentToolset](https://adk.dev/integrations/environment-toolset/)
- [Google AI Studio: API Keys](https://aistudio.google.com/apikey)
