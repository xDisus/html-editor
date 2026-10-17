# Revisão conjunta dos planos 001–004 (2026-10-17)

Aplicada: o bug foi corrigido (U0) e os planos viraram `docs/plans/2026-10-17-005-feat-editor-completo-plan.md`. Os antigos estão em `docs/plans/superseded/`.

## 0. Bug atual que trava os quatro planos

`editor.py` salva buscando `/raw/` de novo a cada clique em Salvar. `/raw/` roda `add_ids` no arquivo **já salvo**.
Se o salvamento anterior criou, apagou ou mudou a ordem de tags, os números `data-edid` mudam. A página aberta ainda usa os números antigos. Então o segundo salvamento grava mudanças no elemento errado.

- Já acontece hoje: Enter dentro de um texto cria `<div>`/`<br>`, salva, edita outro texto mais abaixo, salva de novo.
- Vai piorar muito com os novos planos: spans (001), itens inseridos (003), slides reordenados (004).
- Plano 001 R11 diz "salvar não apaga o histórico". Então editar depois de salvar é o uso normal.
- **Correção (1 linha de ideia):** buscar `/raw/` uma vez só, quando a página abre. Em cada salvamento, usar um clone novo desse original. As marcas `data-edited`/`data-moved` continuam nos elementos, então cada salvamento reaplica tudo sobre a mesma base.
- Fazer isso antes do 001, como passo zero.

## 1. Fundação comum: construir uma vez e usar nos quatro

Os quatro planos pedem as mesmas peças. Hoje cada plano as descreve como se fossem só suas.

| Peça | Quem usa | Ideia preguiçosa |
|---|---|---|
| Desfazer/refazer | 001, 002, 003, 004 | Cada ação guarda um "antes/depois" **só do que tocou**: o `innerHTML` do bloco, a string `style`, ou a lista de filhos do pai. Desfazer = trocar pelo "antes". Não usar um `MutationObserver` no `body` inteiro: os scripts da página (gráficos) e as marcas do próprio editor encheriam a pilha de lixo. |
| Salvar | 001, 002, 003, 004 | Generalizar as 2 marcas atuais em 3: `data-edited` (copia `innerHTML`), `data-styled` (copia `style`; substitui `data-moved` e também cobre formatação de bloco do 001 R7/R8), `data-kids` (pai cujos filhos mudaram: refaz a lista de filhos no original. Filho com `data-edid` = move o nó original. Filho sem = clone limpo. Filho que sumiu = apagado). Uma regra cobre inserir, apagar, duplicar, colar e reordenar slides. |
| Clonar limpo | 003 R11/R12, 004 R7/R8, miniaturas 004 R4 | Uma função só: remove `data-edid`, `id` e marcas do editor. 003 hoje **não** tira ids nem `data-edid`. Clone com `data-edid` faz o salvar gravar por cima do original. Miniatura clonada colocaria ids repetidos na página. |
| "Caixa de fora" / "pode conter caixas" / "slide" | 002 R6/R14, 003 R6/R7, 004 R1 | Uma regra de reconhecer contêiner + a lista de slides do 004. O 003 R7 ("slide no meio da tela") usa essa lista. |
| Teclas e colar por contexto | 002 R10, 003 R3/R9/R11/R12, 004 R7/R9 | Um só tratador de teclas que olha o foco: cursor no texto → comportamento nativo. Caixa selecionada → age na caixa. Miniatura → age no slide. O tratador de `paste` atual (só texto puro) vira esse mesmo tratador. |

Resposta para perguntas que ficaram "para o planejamento":
- 001 "desfazer vs. desfazer nativo": o editor sempre captura Ctrl+Z/Ctrl+Y e agrupa a digitação por pausa. Não usar o nativo.
- 003 "compressão de imagem": `canvas.toBlob`, de graça no navegador. JPEG/WebP ~0.85 para fotos. PNG se tiver transparência. Nenhuma biblioteca.
- 004 "miniaturas sem pesar": clone limpo + `transform: scale()` no CSS. Atualizar só a miniatura do slide atual, quando a pilha de desfazer mudar.

## 2. Conflitos entre os planos

1. **Alt+arrastar.** 001 R10 e AE5 citam esse atalho. 002 o remove. Trocar por "mover caixa" no 001. (O próprio 002 já pede isso.)
2. **Dois grupos de botões de alinhar.** 001 R2 tem alinhamento de texto (esq/centro/dir). 002 R12/R14 tem alinhamento de caixa. Sugestão: os mesmos botões, pelo contexto. Cursor no texto = alinha o texto. Caixa selecionada = alinha a caixa. A barra fica com menos botões.
3. **Formatar com caixa selecionada (sem cursor).** 001 R7 fala só de "bloco onde está o cursor". Com o 002 também existe "caixa selecionada". Definir: vale para a caixa inteira (igual ao PowerPoint).
4. **Ctrl+D e Delete.** 003 e 004 usam os dois atalhos. 004 já resolve pelo foco. Duplicar slide (004 R7) deve ser o duplicar do 003, só que logo depois e sem deslocar. A regra de tirar ids (004 R8) passa a valer também para o 003.
5. **Ctrl+V.** 003 R3 (colar imagem) e R12 (colar caixa) disputam com o colar de texto atual. Resolve com o tratador único do item 1.

## 3. Cortes possíveis (é você quem decide — já estão aprovados)

Você aprovou estes itens na brainstorm. Ficam se você não disser o contrário.

- **Ctrl+C/Ctrl+V de caixas (003 R12).** Ctrl+D já cobre quase tudo dentro do mesmo arquivo. Recomendo: manter só se colar em outro slide for comum.
- **Miniaturas visuais (004 R4).** Uma lista com o título de cada slide resolve achar e reordenar. Recomendo: manter as visuais. Com clone + `scale()` custa poucas linhas.
- **Guias magnéticas (002 R11).** É a parte mais trabalhosa do 002. Recomendo: manter, mas comparar só com caixas irmãs e com a caixa de fora (não com a página inteira).
- **Distribuir (002 R13).** Pequeno. Pode ficar.

## 4. Ordem e risco

- Os quatro mexem só em `editor.py`. Então rodam em fila: 0 (bug do salvar) → 001 → 002 → 003 → 004. O `ship-plans` não consegue rodar em paralelo.
- Colocar a fundação do item 1 no 001 (ou num plano 000 só para ela).
- **Maior risco: 002 R16 (posição proporcional).** O `translate` em % usa o tamanho da própria caixa, não o da caixa de fora. Dentro de linhas e grades automáticas da página isso é difícil. Fazer um teste rápido antes de implementar o 002.
- O JS vai crescer de ~50 para centenas de linhas dentro de uma string Python. Opcional: mover para `editor.js`, lido na inicialização. É um arquivo a mais, mas fica mais fácil de editar.

## 5. Mudanças propostas nos planos (ainda não feitas)

- 001: R10/AE5 sem Alt+arrastar. Somar a seção "Fundação" (desfazer por antes/depois, 3 marcas de salvar, clone limpo, teclas por contexto). Alinhar por contexto. Formatar a caixa selecionada.
- 002: R12/R14 usam os mesmos botões de alinhar do 001. R16 vira teste rápido primeiro.
- 003: R11/R12 usam o clone limpo (sem ids).
- 004: R7 reaproveita o duplicar do 003. R1 compartilha a regra de contêiner com 002/003.
- Novo passo 0: correção do bug do salvar.
