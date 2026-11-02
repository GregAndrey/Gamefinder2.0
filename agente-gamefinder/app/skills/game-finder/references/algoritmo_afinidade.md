# Algoritmo de Afinidade GameFinder: Cálculo de Match (%)

Este documento detalha o sistema de pontuação e lógica de compatibilidade entre o perfil do jogador e os títulos do catálogo.

---

## 1. Regra Preliminar: Filtro Binário de Plataforma

* Se o jogo **não** estiver disponível em nenhuma das plataformas ativas selecionadas pelo jogador (Steam, PlayStation ou Xbox), a pontuação é automaticamente **0%** e o jogo é sumariamente descartado.
* Jogos disponíveis em mais de uma plataforma de posse do jogador ganham destaque de versatilidade.

---

## 2. Composição da Pontuação de Afinidade (0 a 100%)

A pontuação de afinidade é calculada a partir de 4 pilares ponderados:

```
Pontuação Final = (Gênero * 0.35) + (Gameplay/Pacing * 0.30) + (Similaridade com Favoritos * 0.25) + (Comunidade * 0.10) - Penalidades
```

### Pilar 1: Interseção de Gêneros e Ambientação (Peso: 35%)
* **Gênero Principal idêntico:** 20 pontos.
* **Subgênero ou Gênero Secundário:** 10 pontos adicionais.
* **Ambientação compatível** (ex.: Fantasia Medieval, Cyberpunk, Sci-Fi, Pós-apocalíptico): 5 pontos adicionais.
* *Total máximo deste pilar: 35%.*

### Pilar 2: Estilo de Gameplay, Pacing e Rotina (Peso: 30%)
* **Foco de Experiência compatível:**
  * Narrativa / Foco em História: 10 pontos.
  * Combate Desafiador / Mecânico: 10 pontos.
  * Exploração / Mundo Aberto: 10 pontos.
  * Coop / Multiplayer ou Single-Player puro conforme a preferência: 10 pontos.
* **Compatibilidade de Pacing e Rotina:**
  * Jogador com pouco tempo (sessões de < 1h): bônus de 10 pontos para jogos com saves frequentes, ritmo rápido ou campanhas compactas (10-20h).
  * Jogador com tempo amplo: bônus de 10 pontos para campanhas épicas (50h+) e exploração profunda.
* *Total máximo deste pilar: 30%.*

### Pilar 3: Similaridade com Jogos Amados do Histórico (Peso: 25%)
* **Mecânicas e Estrutura idênticas** a jogos amados (ex.: combate estilo Dark Souls, narrativa ramificada estilo The Witcher 3): 15 pontos.
* **Mesmo Estúdio / Direção Criativa** consagrada: 5 pontos adicionais.
* **Tom e Atmosfera similares** (ex.: suspense psicológico, humor irônico, melancolia): 5 pontos adicionais.
* *Total máximo deste pilar: 25%.*

### Pilar 4: Avaliação e Aprovação da Comunidade (Peso: 10%)
* Jogos aclamados pela comunidade (nota ≥ 4.5/5 ou aprovação Steam > 90%): 10 pontos.
* Jogos muito bem avaliados (nota 4.0 a 4.4): 7 pontos.
* Jogos polarizados ou desconhecidos: 4 pontos.
* *Total máximo deste pilar: 10%.*

---

## 3. Modificadores Negativos e Filtros de Aversão

* **Jogos já jogados:** Exclusão automática do feed de novidades (match score não gerado).
* **Mecânicas rejeitadas pelo jogador:**
  * Se o jogador detesta "combate por turnos", "mundo aberto repetitivo com torres", "grinding infinito" ou "perda total de progresso (roguelike punitivo)": penalidade de **-35%** ou descarte imediato do título.
* **Jogos similares a títulos odiados:**
  * Se o jogador marcou "Já joguei e detestei o jogo X", títulos que compartilham o loop central de gameplay de X sofrem penalidade de **-25%**.

---

## 4. Classificação das Recomendações

| Faixa de Match (%) | Classificação | Posicionamento no Feed |
|---|---|---|
| **90% a 100%** | **Match Supremo (Top Escolha)** | Destaque principal no topo do dashboard com card expandido. |
| **80% a 89%** | **Altamente Recomendado** | Corpo principal do feed com destaque visual. |
| **70% a 79%** | **Boa Compatibilidade / Joia de Nicho** | Recomendações complementares ou expansão de horizonte. |
| **Abaixo de 70%** | **Incompatível** | Não apresentar, exceto sob pedido explícito do jogador para "sair da zona de conforto". |

---

## 5. Gerador da Justificativa Transparente ("Por que recomendamos")

Toda recomendação deve sintetizar o cálculo em uma justificativa de 1 a 2 frases no padrão:
> *"Porque você curtiu [Jogo Favorito do Histórico] e prefere [Gênero/Estilo], combinando com seu gosto por [Mecânica/Ambientação específica]."*

Exemplo:
> *"Porque você amou The Witcher 3 e prioriza histórias maduras e envolventes, Baldur's Gate 3 entrega a mesma profundidade de escolhas e ambientação de fantasia sombria, compatível com seu PC e PlayStation 5."*
