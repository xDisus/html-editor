---
title: Editor completo (formatação, seleção, inserir, slides) - Plan
type: feat
date: 2026-10-17
topic: editor-completo
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
status: completed
product_contract_source: ce-brainstorm
execution: code
supersedes:
  - docs/plans/superseded/2026-10-17-001-feat-barra-formatacao-plan.md
  - docs/plans/superseded/2026-10-17-002-feat-selecao-redimensionar-alinhar-plan.md
  - docs/plans/superseded/2026-10-17-003-feat-inserir-elementos-plan.md
  - docs/plans/superseded/2026-10-17-004-feat-gerenciar-slides-plan.md
---

# Editor completo - Plan

## Goal Capsule

- **Objetivo:** levar o editor visual (`editor.py`) de "edita texto e move com Alt" para um editor ao estilo PowerPoint. Ele terá barra fixa, desfazer, formatação, seleção de caixas, mover, redimensionar, alinhar, inserir texto e imagem, e um painel de slides.
- **Origem:** junta os planos 001–004 (em `docs/plans/superseded/`) e a revisão `docs/revisao-planos-2026-10-17.md`. As decisões de produto dos quatro continuam valendo. Este plano só tira duplicações, resolve conflitos e fecha as perguntas que tinham ficado para o planejamento.
- **Já feito (U0):** bug do salvar duas vezes corrigido em `editor.py` (o original é buscado uma vez ao abrir), com teste em `test_editor.py`.
- **Bloqueios em aberto:** nenhum. U3 começa com um teste rápido de posição proporcional (ver U3).

---

## Product Contract

### Summary

Uma barra fixa no topo reúne desfazer, salvar, formatação, alinhar e inserir.
A pessoa seleciona caixas como no PowerPoint. Com elas, move, redimensiona, empurra com as setas e alinha com guias magnéticas.
Um painel lateral de miniaturas cria, duplica, apaga e reordena slides, ou seções de páginas com rolagem.
O arquivo salvo continua um HTML autocontido, sem marcas do editor, que abre igual em qualquer computador e sem internet.

### Problem Frame

A equipe gera dashboards e apresentações em HTML e precisa ajustá-los sem mexer em código.
Os arquivos são apresentados em tela cheia, em projetores e outros notebooks, ou enviados por e-mail (limite comum de 10 MB).
Num HTML qualquer as caixas ficam umas dentro das outras, e scripts da página geram conteúdo que o editor não pode gravar.

### Key Decisions

Decisões dos planos 001–004 que continuam valendo, todas aprovadas pelo usuário:

- Barra fixa no topo, não flutuante. O painel de slides fica na lateral esquerda. Barra e painel só existem no editor.
- Só fontes seguras. Nada de Google Fonts.
- Formatação vale para as palavras selecionadas; sem seleção, vale para o bloco.
- Desfazer só enquanto a página está aberta. O `.bak` cobre o resto.
- O clique funciona como no PowerPoint, sem modos. Um caminho de caixas na barra (como no Dreamweaver) mostra onde a seleção está.
- Posição e tamanho ficam em proporção à caixa de fora. Alt+arrastar deixa de existir, e Alt passa a desligar as guias.
- A imagem fica embutida no HTML e é reduzida automaticamente. Neste plano só entram caixa de texto e imagem.
- Apagar não pede confirmação, porque o desfazer recupera.
- O painel também vale para páginas com rolagem. Um slide novo copia o estilo do atual. Uma cópia não repete identificadores únicos.

Decisões novas desta junção:

- **Uma fundação, usada por tudo (U1).** Desfazer, salvar, clonar e o tratador de teclas são feitos uma vez só. Os quatro planos antigos pediam as mesmas peças.
- **Desfazer por "antes/depois" só do que a ação tocou.** Nada de `MutationObserver` no `body`, porque os scripts da página e as marcas do editor sujariam a pilha.
- **Os mesmos botões de alinhar, conforme o contexto.** Cursor no texto: os botões alinham o texto. Caixa selecionada: alinham a caixa. Isso substitui os grupos separados de 001 R2 e 002 R12/R14.
- **Formatar com caixa selecionada (sem cursor no texto) vale para a caixa inteira.** É o que acontece no PowerPoint.
- **Duplicar é uma ação só, para caixa e para slide.** O slide sai logo depois do original, sem deslocamento. A caixa sai deslocada.
- **A interface do editor sai da string Python** e vai para `editor-ui.html`, lido na inicialização. São centenas de linhas, e editar JS dentro de uma string Python atrapalha.

### Requirements

IDs novos. Entre parênteses, de onde cada um veio.

**Fundação**

- F1. O desfazer e o refazer funcionam pelos botões e por Ctrl+Z, Ctrl+Y e Ctrl+Shift+Z. Eles voltam qualquer ação do editor na ordem em que aconteceu. (001 R9, R10; 002 R17; 003 R14; 004 R12)
- F2. Salvar não apaga o histórico. Recarregar a página apaga. (001 R11)
- F3. Tudo o que a pessoa muda aparece no arquivo salvo: texto, formatação, posição, tamanho, itens novos, apagados, duplicados e reordenados. (001 R12; 002 R15; 003 R13; 004 R11)
- F4. O arquivo salvo continua autocontido, sem marcas do editor e sem nada que dependa de internet. Conteúdo gerado por scripts da página nunca é gravado. (001 R13)
- F5. Salvar várias vezes sem recarregar sempre grava no elemento certo. (bug U0)

**Barra e texto**

- T1. Uma barra fixa no topo mostra sempre desfazer, refazer e salvar. Ela também reúne fonte, tamanho, negrito, itálico, alinhar e inserir. (001 R1, R2; 003 R1)
- T2. O seletor de fonte tem Arial, Verdana, Tahoma, Trebuchet MS, Georgia, Times New Roman e Courier New. Se o texto usa outra fonte, o seletor mostra o nome dela e não muda nada. (001 R3, R4)
- T3. O tamanho tem uma lista (10, 12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 64, 72) e também aceita qualquer número. (001 R5; fecha a pergunta em aberto)
- T4. Fonte, tamanho, negrito e itálico valem para as palavras selecionadas. Sem palavras selecionadas, valem para o bloco do cursor. Com uma caixa selecionada, valem para a caixa inteira. (001 R6, R7)
- T5. Com o cursor no texto, os botões de alinhar mudam o alinhamento do bloco inteiro: esquerda, centro e direita. (001 R8)

**Seleção, mover, redimensionar e alinhar**

- S1. Um clique numa caixa a seleciona e mostra alças. Um segundo clique, ou um duplo clique, põe o cursor no texto. Esc no texto sai da edição e deixa a caixa selecionada. (002 R1–R3)
- S2. Shift+clique adiciona caixas à seleção ou as tira dela. O clique seleciona a caixa mais de dentro. (002 R4, R5)
- S3. A barra mostra o caminho de caixas, por exemplo `slide › card › título`. Clicar num item do caminho, ou apertar Esc com uma caixa selecionada, seleciona a caixa de fora. (002 R6)
- S4. Arrastar uma caixa selecionada a move, e as vizinhas não se mexem. Puxar uma alça muda o tamanho, e com Shift a proporção fica mantida. A caixa nunca fica menor que o texto dela. (002 R7–R9)
- S5. As setas empurram a caixa 1 px, e Shift+seta empurra 10 px. Com o cursor no texto, as setas movem o cursor. (002 R10)
- S6. Guias magnéticas aparecem quando a caixa se alinha pela borda ou pelo centro com uma caixa irmã ou com a caixa de fora. A caixa gruda a até 6 px de tela. Alt desliga as guias. (002 R11)
- S7. Com uma caixa selecionada, os botões de alinhar a posicionam dentro da caixa de fora. Com duas ou mais, alinham pela esquerda, centro, direita, topo, meio ou base. Com três ou mais, distribuem na horizontal ou na vertical. (002 R12–R14)
- S8. Posição e largura ficam em proporção à caixa de fora. (002 R16)

**Inserir, apagar, duplicar, copiar e colar**

- I1. A barra insere caixa de texto ("Digite aqui" já selecionado) e imagem (pela escolha de arquivo, ou com Ctrl+V fora de um texto). (003 R1–R3)
- I2. A imagem fica embutida como `data:`. Imagens com mais de 1920 px de largura são reduzidas para 1920. As que têm transparência viram PNG. As outras viram JPEG com qualidade 0.85. (003 R4, R5; fecha a pergunta em aberto)
- I3. O item novo entra na caixa selecionada se ela for um contêiner. Se não for, entra na caixa de fora dela. Sem nada selecionado, entra no slide do meio da tela. Ele aparece centralizado, por cima dos outros e já selecionado. (003 R6–R8)
- I4. Delete ou Backspace apaga as caixas selecionadas, sem pedir confirmação. Com o cursor no texto, as teclas apagam letras. (003 R9, R10)
- I5. Ctrl+D duplica as caixas selecionadas. Ctrl+C e Ctrl+V copiam e colam caixas no mesmo arquivo, seguindo I3. As cópias não repetem `id`. (003 R11, R12; regra do 004 R8 estendida)

**Slides**

- L1. O editor reconhece os slides: os blocos grandes que se repetem no primeiro nível da página. Com dois ou mais, aparece um painel de miniaturas à esquerda, que pode ser recolhido. (004 R1–R3)
- L2. As miniaturas mostram a aparência atual do slide. Clicar numa miniatura leva a página até aquele slide e o marca como atual. (004 R4, R5)
- L3. "Slide novo" cria, logo depois do slide atual, um slide com o mesmo estilo, vazio, com o título "Novo slide". (004 R6)
- L4. Com a miniatura selecionada, Ctrl+D (ou o botão) duplica o slide, e Delete (ou o botão) apaga. O último slide não pode ser apagado. Arrastar uma miniatura reordena os slides. (004 R7, R9, R10)

### Acceptance Examples

- AE1. **F5.** **Given** a pessoa edita o 1º parágrafo e cria uma tag nova, e depois salva. **When** edita o último parágrafo e salva de novo, **then** os dois textos ficam no lugar certo. (coberto em `test_editor.py`)
- AE2. **T4.** **Given** o título "Resultados do trimestre". **When** a pessoa seleciona "trimestre" e clica em negrito, **then** só essa palavra fica em negrito.
- AE3. **T5, S7.** **Given** o cursor num parágrafo. **When** a pessoa clica em centralizar, **then** o texto fica centralizado. **Given** a caixa selecionada (sem cursor). **When** clica em centralizar, **then** a caixa vai para o centro da caixa de fora.
- AE4. **T2.** **Given** um texto com uma fonte do Google. **When** a pessoa clica nele, **then** o seletor mostra essa fonte e nada muda.
- AE5. **F1, F2.** **Given** a pessoa moveu um card, salvou e deixou um texto em itálico. **When** aperta Ctrl+Z duas vezes, **then** o itálico some e depois o card volta ao lugar.
- AE6. **S1, S3.** **Given** um título dentro de um card dentro de um slide. **When** a pessoa clica no título, clica de novo e aperta Esc três vezes, **then** a sequência é: título selecionado, cursor no texto, título selecionado, card selecionado, slide selecionado. O caminho na barra acompanha cada passo.
- AE7. **S6.** **Given** dois cards lado a lado. **When** a pessoa arrasta um até o topo dele ficar perto do topo do outro, **then** aparece uma guia e os topos se alinham. **When** faz o mesmo com Alt, **then** não aparece guia.
- AE8. **S7.** **Given** três cards em alturas diferentes selecionados. **When** a pessoa alinha pelo topo e distribui na horizontal, **then** os três ficam com o mesmo topo e o mesmo espaço entre eles.
- AE9. **S8.** **Given** um card movido para a direita num notebook. **When** o arquivo salvo abre numa tela mais larga, **then** o card fica na mesma posição relativa ao slide.
- AE10. **I2.** **Given** uma foto de 4000 px e 5 MB. **When** a pessoa a insere e salva, **then** a imagem tem no máximo 1920 px e o arquivo cresce bem menos que 5 MB.
- AE11. **I3.** **Given** um título selecionado dentro de um card. **When** a pessoa insere uma imagem, **then** a imagem entra no card, não no título. **Given** nada selecionado e a página no 3º slide, **then** o item entra no 3º slide.
- AE12. **I4, F1.** **Given** um card original selecionado. **When** a pessoa aperta Delete e depois Ctrl+Z, **then** o card some sem aviso e volta no mesmo lugar. Salvar depois disso não perde o card.
- AE13. **L1.** **Given** uma página com rolagem de quatro seções, **then** o painel mostra quatro miniaturas. **Given** uma página de um bloco só, **then** o painel não aparece.
- AE14. **L3.** **Given** o slide 2 (fundo azul) como atual. **When** a pessoa clica em slide novo, **then** surge o slide 3 com fundo azul e "Novo slide", e os slides seguintes descem uma posição.
- AE15. **L4, F3.** **Given** cinco slides. **When** a pessoa arrasta a miniatura do 5 para o topo e salva, **then** o arquivo abre com aquele slide primeiro.
- AE16. **I5, F4.** **Given** um slide com um gráfico gerado por script e um `id`. **When** a pessoa duplica o slide e salva, **then** o original continua funcionando, a cópia não tem `id`, e a área do gráfico na cópia fica vazia (nada gerado por script é gravado).

### Scope Boundaries

- Ficam fora: cores, bordas, cantos e espaçamento; Google Fonts; histórico que sobrevive ao recarregar.
- Ficam fora: grade fixa, girar caixas e agrupar caixas.
- Ficam fora: formas e tabelas, trocar uma imagem existente, imagem por link, e copiar ou colar entre arquivos.
- Ficam fora: menu de layouts, navegação de apresentação, transições e mover slides entre arquivos.
- Ficam fora: celular e toque.
- Texto gerado por scripts continua não editável.
- Arquivos já salvos pelo editor antigo, com `transform: translate()` em px, continuam funcionando. Eles não são convertidos.

---

## Technical Design

Tudo fica no navegador, dentro de `editor-ui.html`, num objeto `window.ed`. Os testes chamam esse objeto. `editor.py` só serve os arquivos e salva.

### Marcas no DOM (só na página aberta, nunca no arquivo)

| Marca | Significa | No salvar |
|---|---|---|
| `data-edid` | nº da tag no original (já existe) | localiza o nó no original |
| `data-edited` | o texto mudou (já existe) | copia o `innerHTML` limpo |
| `data-styled` | o `style` mudou (substitui `data-moved`) | copia o atributo `style` |
| `data-kids` | os filhos mudaram (inserir, apagar, duplicar, reordenar) | refaz a lista de filhos (abaixo) |
| `data-ed-new` | o nó foi criado pelo editor | entra no salvar como clone limpo |
| `data-ed` | é interface do editor (já existe) | nunca entra |

**Salvar `data-kids`:** para o pai P no original, percorrer os filhos de P na página:
- filho com `data-edid`: usar o nó do original com aquele número;
- filho com `data-ed-new`: usar um clone limpo;
- nó de texto: copiar;
- qualquer outro filho: pular, porque foi gerado por script.

Depois, `P.replaceChildren(...)`. Filhos que sumiram da página somem do original.

Ordem no salvar: primeiro `data-kids` (de fora para dentro), depois `data-edited` e por último `data-styled`. Toda busca é `doc.querySelector('[data-edid="n"]')`, que acha o nó em qualquer lugar.

### Desfazer

```js
ed.act(label, fn)      // roda fn, que registra o que mexe por ed.touch(...)
ed.touch(el, kind)     // kind: 'html' | 'style' | 'kids'; grava o "antes" e põe a marca
```

`act` grava o "depois" de cada item tocado e empilha `{label, items}`. Desfazer põe o "antes" de volta; refazer põe o "depois".
- `html`: string do `innerHTML`.
- `style`: string do `style`.
- `kids`: array de nós filhos, restaurado com `replaceChildren`. Ele guarda as referências, então o card apagado volta como o mesmo nó, com o mesmo `data-edid`.

A digitação vira um `act` por bloco. O "antes" é gravado no primeiro `beforeinput` depois de 1 s parado ou depois de trocar de bloco. Não usar `input`: ele dispara depois que a letra já entrou. Ctrl+Z e Ctrl+Y são sempre capturados pelo editor. O desfazer nativo do navegador não é usado.

`ed.onchange(cb)` avisa a cada empilhar, desfazer ou refazer. As miniaturas usam esse aviso.

### Peças comuns

- `ed.cleanClone(el)`: clona e primeiro descarta os descendentes sem `data-edid` e sem `data-ed-new`, porque foram gerados por script (F4). Não descarta nada dentro de um bloco `[data-edited]`, porque texto digitado não tem número. Depois tira `data-edid`, `id`, `contenteditable` e as marcas `data-ed*`/`data-edited`/`data-styled`/`data-kids`. Usado em duplicar, copiar, miniaturas e no salvar.
- `ed.isContainer(el)`: elemento de bloco (display ≠ inline) sem texto próprio direto. É o inverso da regra atual do `contenteditable`.
- `ed.outer(el)`: o ancestral contêiner mais próximo.
- `ed.slides()`: desce do `body` pelos wrappers de um filho só. No primeiro nível com 2 ou mais filhos de elemento, slides = o maior grupo de mesma tag + 1ª classe, com 2 ou mais membros e cada um com pelo menos 30% da altura da janela.
- Um só `keydown` em captura decide pelo contexto:
  - cursor num texto: comportamento nativo, menos Ctrl+Z e Ctrl+Y;
  - caixa selecionada: a ação vale para a caixa;
  - foco no painel: a ação vale para o slide.
- Um só `paste` decide assim:
  - imagem na área de transferência e cursor fora de um texto: insere a imagem;
  - caixas copiadas pelo editor e cursor fora de um texto: cola as caixas;
  - cursor num texto: cola só o texto, como hoje.

### Posição proporcional (S8)

- Mover usa `position: relative; left: X%; top: Y%`. O `left` em % usa a largura da caixa de fora, e `relative` não empurra as vizinhas.
- O `top` em % só funciona se a caixa de fora tiver altura definida. Se não tiver (`auto`), `top` fica em px. `ponytail: top em px quando o pai tem altura auto; usar % da largura via margin se aparecer caso real`.
- O tamanho usa `width` em % e `min-height` em px. Por isso o texto nunca fica cortado (S4).
- Uma caixa com `position: absolute` ou `fixed` própria continua assim. O editor só ajusta os `left` e `top` dela.

---

## Implementation Units

Fila única, todos os passos em `editor.py` e `editor-ui.html`. Cada passo deixa `python3 test_editor.py` passando e acrescenta seus próprios testes ali (Playwright, chamando `window.ed` e usando `docs/slides.html` e `docs/dash.html`).

### U0. Bug do salvar duas vezes — FEITO

- `editor.py`: `/raw/` é buscado uma vez ao abrir; cada salvamento parte de um `DOMParser` novo sobre essa mesma string.
- `test_editor.py`: AE1.

### U1. Fundação

- `editor.py`: a constante `JS` vira `open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "editor-ui.html")).read()`. O snippet vai para `editor-ui.html` sem mudar nada.
- Barra fixa no topo, da largura da tela, com desfazer, refazer e salvar. `body{margin-top}` só no estilo `data-ed` do editor.
- `ed.act`/`ed.touch`/desfazer/refazer/`ed.onchange`, digitação agrupada, Ctrl+Z/Y/Shift+Z.
- Salvar com as marcas da tabela. `data-moved` vira `data-styled`.
- `ed.cleanClone`, `ed.isContainer`, `ed.outer`, `ed.slides`, um só `keydown` e um só `paste`.
- O Alt+arrastar continua até o U3, mas já passa por `ed.act` (com `touch` do tipo `style`).
- **Testes:**
  - editar texto, Ctrl+Z, conferir o texto antigo;
  - mover com Alt, salvar e desfazer, conferir que a pilha sobrevive ao salvar (F2);
  - remover um filho via `ed.act` + `touch(kids)`, salvar e conferir que sumiu do arquivo; desfazer, salvar e conferir que voltou;
  - um nó gerado por script dentro de um pai `data-kids` não vai para o arquivo (F4).

### U2. Formatação (T1–T5)

- Fonte: `<select>` com as 7 fontes e uma opção extra que mostra a fonte atual quando ela não está na lista (via `getComputedStyle`).
- Tamanho: `<input list>` + `<datalist>` com a lista de T3. Isso é nativo e cobre a lista e o número livre.
- Com palavras selecionadas: `execCommand('styleWithCSS', true)` e depois `bold`, `italic` e `fontName`. Para o tamanho, `execCommand('fontSize', 7)` e trocar os `font-size: xxx-large` gerados pelo valor em px. `ponytail: execCommand é obsoleto mas funciona em todos os navegadores; trocar por Range manual se algum navegador remover`.
- Sem palavras selecionadas, ou com uma caixa selecionada: `style` do bloco ou da caixa, com `touch(style)`.
- Alinhar: com o cursor no texto, `text-align` no bloco. O alinhamento de caixa vem no U3, nos mesmos botões.
- Toda formatação de palavras passa por `act` + `touch(html)` no bloco.
- **Testes:** AE2, AE4, Georgia no bloco sem seleção, salvar e conferir o `style` no arquivo, Ctrl+Z da formatação.

### U3. Seleção, mover, redimensionar e alinhar (S1–S8)

- **Começar pelo teste rápido de S8:** mover um card dentro de `section` (bloco) e dentro de um pai flex/grid em `docs/dash.html`. Salvar, abrir com 1280 e 1920 px de largura e comparar a posição relativa (AE9). Conferir também uma caixa que tem filhos `position: absolute`: o `position: relative` novo faz deles filhos dela, e eles podem pular de lugar. Se o `top` em % falhar no pai sem altura definida, aplicar o caso de px já descrito e seguir.
- Estado: `ed.sel` (array) e `ed.editing` (elemento ou null). Alças e guias são `div` com `data-ed`, colocadas por `getBoundingClientRect`.
- Clique, segundo clique, Esc, Shift+clique e o caminho de caixas na barra (S1–S3).
- Arrastar e alças, com Shift mantendo proporção. O mínimo vem de `scrollHeight` (S4). Setas (S5).
- Guias: comparar bordas e centros só com as irmãs e com `ed.outer`, a 6 px de tela, desligadas com Alt (S6).
- Alinhar e distribuir (S7) com os mesmos botões de alinhar do U2, que mudam conforme o contexto.
- Remover o Alt+arrastar antigo e a linha dele no `README.md`.
- **Testes:** AE3 (parte da caixa), AE5, AE6, AE7, AE8, AE9, setas no texto vs na caixa.

### U4. Inserir, apagar, duplicar, copiar e colar (I1–I5)

- Caixa de texto: `div` com `data-ed-new` e "Digite aqui" selecionado. Entra pelo `ed.act` com `touch(kids)` no destino (I3), centralizada, com `z-index` acima e já selecionada.
- Imagem: `<input type="file" accept="image/*">` e o `paste`. Desenhar num `canvas` limitado a 1920 px. Se algum pixel tiver alfa < 255, usar `toDataURL('image/png')`; se não, `'image/jpeg', 0.85` (I2).
- Delete/Backspace com caixa selecionada (I4). Ctrl+D com `ed.cleanClone` + `data-ed-new`, deslocado 16 px. Ctrl+C guarda clones limpos na memória da página; Ctrl+V cola pelo I3 (I5).
- **Testes:** AE10 (imagem gerada no teste com `canvas` 4000 px), AE11, AE12, Backspace no texto apaga uma letra, a cópia não tem `id`.

### U5. Painel de slides (L1–L4)

- O painel é um `aside` com `data-ed`, preso à esquerda, e pode ser recolhido. `body{margin-left}` fica só no estilo do editor. O painel só aparece se `ed.slides().length >= 2`.
- Miniatura: `ed.cleanClone(slide)` dentro de uma caixa com `transform: scale()` e `pointer-events: none`. Ela é refeita só para o slide atual, depois de `ed.onchange` (com 300 ms de espera). `ponytail: refaz só a miniatura do slide atual; refazer todas se um script mudar vários slides`.
- Clique na miniatura: `scrollIntoView` e marca o slide como atual.
- Slide novo: `cleanClone(atual)` sem os filhos, mais um `h1` com "Novo slide". Entra logo depois do atual, pelo `touch(kids)` no pai (L3).
- Duplicar e apagar usam o mesmo código do U4, agindo sobre o slide, sem deslocamento e com a posição logo depois. O apagar fica desativado quando só resta 1 slide (L4).
- Reordenar: `draggable` nativo nas miniaturas e `touch(kids)` no pai dos slides.
- **Testes:** AE13 (`docs/slides.html` e uma página de um bloco só criada no teste), AE14, AE15, AE16, apagar desativado com 1 slide.

---

## Verification

- `python3 test_editor.py` passa depois de cada unidade.
- No fim de cada unidade, abrir o arquivo salvo direto no navegador, sem o editor. Ele precisa ter a mesma aparência e nenhum `data-ed*`, `data-edid` ou `contenteditable`.
- Precisa de Playwright para testar: `pip install playwright`. O `editor.py` continua só stdlib.

## Risks

- **S8 em layouts automáticos** é o maior risco. Por isso o teste rápido no começo do U3.
- **`execCommand`** é obsoleto. Funciona hoje e tem saída mapeada (comentário `ponytail:` no U2).
- **Apagar um nó do original** pode quebrar um script da página. Isso foi aceito no 003, e o desfazer recupera.
- **Scripts que contam slides** podem não ver slides novos até reabrir o arquivo. Isso foi aceito no 004.

---

## Achados de execução

- U1–U5 entregues juntos em `editor-ui.html` (branch `feat/editor-completo`); `python3 test_editor.py` roda 12 cenários (AE1–AE16).
- `<h1>` já é negrito por padrão: o botão N numa palavra de título alterna para `font-weight: normal`. É o comportamento do PowerPoint, mas AE2 foi testado num parágrafo.
- Com 1 slide sobrando, `ed.slides()` devolve `[]` (grupo precisa de 2+): o painel some e "apagar" fica sem efeito. Desfazer continua funcionando.
- Miniaturas não reaplicam seletores do tipo `:nth-child` da página; só copiam a cor de fundo calculada.
- Reordenar arrastando miniaturas usa o `draggable` nativo; testado pela API `ed.moveSlide`, não por arrasto real.
- `ponytail:` `top` em px quando o pai tem altura auto; setas não agrupam desfazer (1 passo por toque).
- Review P2 em aberto: resize só usa `min-height` (caixa com `height` fixo não encolhe); mover em páginas com `transform: scale` erra o delta; setas não agrupam desfazer; miniaturas de slides não atuais ficam velhas após desfazer; mouseup fora da janela deixa a ação aberta (`undo` agora ignora enquanto aberta).
