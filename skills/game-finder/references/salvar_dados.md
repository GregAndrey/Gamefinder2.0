# Salvar Recomendações e Wishlist em Arquivo (EnvironmentToolset)

O agente salva a lista de recomendações e desejos do usuário num arquivo CSV utilizando as ferramentas de arquivo do **EnvironmentToolset** do ADK ([adk.dev/integrations/environment-toolset](https://adk.dev/integrations/environment-toolset/)). As ferramentas operam dentro da pasta segura do ambiente (o `working_dir`), permitindo persistência de dados e controle de histórico.

---

## Ferramentas Disponíveis

| Ferramenta | Para que serve | Argumentos |
|---|---|---|
| `WriteFile` | Grava um novo arquivo ou **sobrescreve** o arquivo inteiro com dados atualizados | `path` (texto), `content` (texto) |
| `ReadFile` | Lê um arquivo existente e retorna o conteúdo linha a linha | `path` (texto), `start_line` e `end_line` (opcionais) |

Use **apenas** essas duas ferramentas. O agente não tem permissão e nem necessidade de executar comandos de shell (`Execute`) ou editar trechos isolados (`EditFile`): a lista é sempre regravada íntegra de uma vez.

## Regras de Caminho

* Use sempre o caminho **relativo** `wishlist.csv`. Ele é automaticamente resolvido dentro da pasta `dados/` configurada no ambiente.
* **Nunca** utilize caminhos absolutos (`C:\...` ou `/home/...`) nem navegação com `../`. O ambiente do ADK bloqueia essas tentativas com o erro `Path escapes working directory`.
* Use sempre o mesmo nome de arquivo (`wishlist.csv`). Quando o usuário refinar sugestões ou descartar jogos, a versão atualizada substitui a anterior.

## Como Gravar a Lista de Recomendações e Desejos

1. Estruture os dados de acordo com os títulos recomendados na conversa.
2. Antes de chamar a ferramenta, confira o checklist obrigatório:
   - [ ] A primeira linha é rigorosamente o cabeçalho: `Title,Platforms,Genre,Match Score,Why Recommended,Status`.
   - [ ] Há uma linha por jogo recomendado ou salvo na wishlist, sem linhas em branco intercaladas.
   - [ ] A coluna `Platforms` lista as plataformas separadas por barra ou espaço (ex.: `Steam / PS5 / Xbox`).
   - [ ] A coluna `Match Score` informa o percentual numérico (ex.: `98%`).
   - [ ] Os campos com texto livre (`Why Recommended`) e plataformas estão **obrigatoriamente entre aspas duplas** para proteger vírgulas internas.
   - [ ] A coluna `Status` indica `Recomendado`, `Top Escolha`, `Quero Jogar (Wishlist)` ou `Descartado`.
   - [ ] O conteúdo enviado **não** inclui blocos de código ```` ```csv ````, apenas o texto bruto CSV com quebra de linha final `\n`.
3. Chame a ferramenta `WriteFile` com `path="wishlist.csv"` e `content` contendo o CSV montado.

### Exemplo de Chamada da Ferramenta

```json
{
  "path": "wishlist.csv",
  "content": "Title,Platforms,Genre,Match Score,Why Recommended,Status\nBaldur's Gate 3,\"Steam / PS5 / Xbox Series X|S\",CRPG,98%,\"Porque você amou The Witcher 3 e busca narrativa densa com escolhas reais e temática medieval sombria.\",Top Escolha\nElden Ring,\"Steam / PS4 / PS5 / Xbox Series X|S\",Soulslike / RPG,94%,\"Combate técnico desafiador e exploração rica de fantasia sombria.\",Recomendado\nCyberpunk 2077,\"Steam / PS5 / Xbox Series X|S\",RPG de Ação,88%,\"Excelente escrita de missões, ambientação imersiva e escolhas morais.\",Recomendado\n"
}
```

## Como Interpretar a Resposta da Ferramenta

| Resposta da ferramenta | Ação do Agente |
|---|---|
| `{"status": "ok", "message": "Wrote wishlist.csv"}` | Sucesso confirmado. Informe no template o arquivo gravado e a quantidade de títulos na lista. |
| `{"status": "error", "error": "Path escapes working directory: ..."}` | Caminho inválido. Corrija imediatamente usando o caminho relativo `wishlist.csv`. |
| Qualquer outro erro | Informe gentilmente que houve um problema na gravação em disco e exiba o CSV em bloco formatado no corpo da resposta. |

> **Atenção:** Nunca afirme ao usuário que a lista foi gravada com sucesso sem ter recebido a resposta `"status": "ok"` da ferramenta `WriteFile`.

## Refinamento, Descarte e Atualização de Histórico

1. Quando o usuário pedir para descartar um título ("Não quero jogar o jogo X, prefiro outro"), chame `ReadFile` em `wishlist.csv` para inspecionar os títulos já cadastrados (caso necessário).
2. Substitua o título rejeitado pelo novo título recomendado com sua respectiva justificativa.
3. Se o usuário quiser marcar um título como "Quero Jogar (Wishlist)" ou registrar uma avaliação, atualize o status da linha correspondente.
4. Chame `WriteFile` com a lista inteira atualizada em `wishlist.csv`.
5. Confirme ao usuário a atualização do arquivo e as novidades inseridas.
