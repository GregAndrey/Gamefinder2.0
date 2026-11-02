# Fluxo de Trabalho: Sistema de Recomendação GameFinder

Siga os passos na ordem. Não pule etapas e não exiba cálculos matemáticos brutos na resposta para o usuário, a menos que ele solicite. Apresente o resultado final formatado de acordo com o template de saída.

---

## Passo 1: Triagem de Perfil e Filtro Rígido de Plataforma

Com as informações coletadas no gating:

1. **Mapeamento de Plataformas Ativas:** Identifique as plataformas que o usuário possui (Steam, PlayStation, Xbox).
   * **Regra Rígida:** Elimine imediatamente do radar qualquer título exclusivo que não esteja disponível em pelo menos uma das plataformas ativas do jogador.
2. **Definição de Persona:**
   * *Jogador com Tempo Limitado:* priorize jogos com bom ritmo inicial (que prendam nos primeiros 30 minutos), campanhas moderadas (10 a 25 horas) ou estrutura em sessões curtas/roguelites.
   * *Entusiasta Multiplataforma:* compare onde o jogo roda melhor ou destaque disponibilidade cruzada.
   * *Explorador de Nichos/Indies:* destaque joias escondidas, metroidvanias, roguelikes e indies premiados em vez de blockbusters óbvios.
   * *Jogador Social/Comunidade:* dê peso extra às avaliações da comunidade e modos cooperativos.

## Passo 2: Cálculo de Afinidade e Filtros de Exclusão

1. Use a ferramenta `load_skill_resource` para ler `references/algoritmo_afinidade.md`.
2. Aplique os filtros de exclusão:
   * **Títulos já jogados:** remova jogos que o usuário informou no histórico de "Já joguei".
   * **Exclusão de aversão:** se o usuário marcou títulos como "Já joguei e não curti" ou expressou aversão a certas mecânicas (ex.: grinding repetitivo, combate por turnos, puzzles sem combate), reduza o peso ou exclua títulos com mecânicas similares.
3. Calcule o **Índice de Match (%)** de compatibilidade entre o perfil do usuário e os jogos elegíveis.

## Passo 3: Consulta ao Catálogo e Curadoria

1. Use a ferramenta `load_skill_resource` para ler `references/catalogo_jogos.md`.
2. Selecione de **3 a 5 recomendações principais**, garantindo diversidade:
   * **1 Top Escolha (Match Supremo):** o título com maior aderência e compatibilidade direta com os favoritos do usuário.
   * **2 a 3 Recomendações Fortes:** títulos de alta sinergia com os gêneros e estilo de gameplay solicitados.
   * **1 Sugestão Alternativa / Joia Escondida (opcional mas recomendado):** um indie aclamado ou título de nicho que compartilhe os pilares essenciais de gameplay, expandindo os horizontes do jogador.

## Passo 4: Ficha Técnica e Justificativa Transparente ("Por que recomendamos")

Para cada título selecionado, formule uma justificativa contextual e honesta:
* Conecte o jogo a referências concretas citadas pelo jogador (ex.: *"Porque você amou The Witcher 3 e busca uma ambientação de fantasia sombria com escrita madura"*).
* Destaque o pilar de gameplay mais relevante (ex.: combate desafiador soulslike, escolhas com consequências reais, exploração sem marcadores no mapa).
* Informe a estimativa de duração da campanha principal e estilo de ritmo (pacing).

## Passo 5: Montagem da Resposta e Persistência em Arquivo

1. Use `load_skill_resource` para ler `assets/recomendacao_template.md`.
2. Preencha todas as seções do template na ordem especificada.
3. Monte o CSV de lista de desejos/recomendações com os títulos sugeridos.
4. Use `load_skill_resource` para ler `references/salvar_dados.md` e execute a chamada da ferramenta `WriteFile` salvando os dados em `wishlist.csv` dentro do ambiente de trabalho.
   * Se a ferramenta `WriteFile` não estiver disponível, exiba o bloco de dados no formato especificado no template.
5. Na resposta, confirme a gravação do arquivo e apresente a quantidade de jogos salvos.

## Passo 6: Refinamento, Descarte e Feedback Contínuo

Após a entrega das recomendações, o usuário pode interagir:
* **"Não gostei dessa recomendação / já conheço esse jogo":** descarte o jogo específico, recalibre os pesos e sugira um substituto imediato com justificativa.
* **"Adicionar à minha wishlist":** confirme a priorização do título.
* **"Quero avaliar um jogo que já zerei":** registre a nota (1 a 5 estrelas) e comentário do usuário, recalculando o perfil de gosto para futuras consultas.
* A cada refinamento ou alteração na lista de desejos, atualize a tabela de recomendações na conversa **e** regrave o arquivo `wishlist.csv` usando `WriteFile`.
