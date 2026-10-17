---
title: Selecao, redimensionar e alinhar - Plan
type: feat
date: 2026-10-17
topic: selecao-redimensionar-alinhar
artifact_contract: ce-unified-plan/v1
artifact_readiness: requirements-only
product_contract_source: ce-brainstorm
execution: code
---

# Selecao, redimensionar e alinhar - Plan

## Goal Capsule

- **Objetivo:** permitir selecionar caixas no editor visual (`editor.py`) e, com elas, mover, redimensionar, empurrar com as setas, alinhar com guias magnéticas e alinhar ou distribuir várias pela barra.
- **Autoridade de produto:** decisões tomadas com o usuário nesta brainstorm. Formatação de texto e desfazer (plano 001), inserir elementos e gerenciar slides não fazem parte deste plano.
- **Bloqueios em aberto:** nenhum.

---

## Product Contract

### Summary

A pessoa seleciona caixas como no PowerPoint: um clique seleciona, clicar de novo edita o texto.
Com a caixa selecionada, ela move, redimensiona, empurra com as setas e alinha com guias magnéticas ou pelos botões da barra.
Um caminho de caixas na barra mostra onde a seleção está e deixa subir para a caixa de fora.

### Problem Frame

Hoje o editor só edita texto com um clique e move com Alt+arrastar, sem ver o que está selecionado.
Não dá para mudar tamanho, alinhar uma caixa com outra nem posicionar com precisão.
Num HTML qualquer as caixas ficam umas dentro das outras (slide, card, título), então "clicar numa caixa" é ambíguo.
Os arquivos são apresentados em telas diferentes da tela onde foram editados, como projetores e outros notebooks.

### Key Decisions

- **Clique ao estilo PowerPoint, sem modos.** A equipe já conhece esse padrão e ninguém precisa lembrar em que modo está. (session-settled: user-approved — chosen over dois modos Texto/Organizar na barra e Alt+clique: sem atalho escondido nem estado de modo) Governs R1, R2, R3, R4.
- **Caminho de caixas na barra, ideia do Dreamweaver.** Resolve caixas aninhadas sem adivinhar qual delas a pessoa queria. (session-settled: user-approved — chosen over só o clique: o HTML aninha caixas e o clique sozinho não sabe qual pegar) Governs R5, R6.
- **Posição e tamanho proporcionais à caixa de fora.** A caixa acompanha o resto da página quando a tela muda de tamanho. (session-settled: user-directed — chosen over pixels fixos e escolha por caixa: os arquivos são apresentados em projetores e outros notebooks) Governs R16.
- **Alt+arrastar deixa de existir.** Arrastar a caixa selecionada já move, e Alt passa a desligar as guias. Governs R7, R11.

### Requirements

**Selecionar**

- R1. Um clique numa caixa a seleciona e mostra alças nos cantos e lados.
- R2. Clicar de novo numa caixa selecionada, ou dar duplo clique, coloca o cursor no texto para editar.
- R3. Esc com o cursor no texto sai da edição e deixa a caixa selecionada.
- R4. Shift+clique adiciona ou remove caixas da seleção.
- R5. O clique seleciona a caixa mais de dentro no ponto clicado.
- R6. A barra mostra o caminho da caixa selecionada até a página (por exemplo `slide › card › título`); clicar num item do caminho, ou apertar Esc com a caixa selecionada, seleciona a caixa de fora.

**Mover e redimensionar**

- R7. Arrastar uma caixa selecionada a move; as caixas vizinhas não se mexem.
- R8. Puxar uma alça muda largura e altura; com Shift, a proporção fica mantida.
- R9. Se a caixa ficar menor que o texto dela, ela cresce para baixo, e o texto nunca fica cortado.
- R10. Com uma caixa selecionada, as setas a empurram 1 pixel e Shift+seta empurra 10 pixels; com o cursor no texto, as setas movem o cursor.

**Guias magnéticas**

- R11. Ao mover ou redimensionar, aparecem linhas quando a caixa alinha pela borda ou pelo centro com outra caixa ou com a caixa de fora, e a caixa gruda nessa posição; segurar Alt desliga as guias.

**Alinhar e distribuir pela barra**

- R12. Com duas ou mais caixas selecionadas, a barra alinha pela esquerda, centro, direita, topo, meio ou base da seleção.
- R13. Com três ou mais caixas selecionadas, a barra distribui as caixas com o mesmo espaço entre elas, na horizontal ou na vertical.
- R14. Com uma caixa só, os botões de alinhar a posicionam dentro da caixa de fora.

**Arquivo salvo e outras telas**

- R15. Movimentos, tamanhos e alinhamentos aparecem no arquivo salvo, que continua autocontido e sem marcas do editor.
- R16. Posição e tamanho ficam guardados em proporção à caixa de fora, para acompanhar telas de outro tamanho.
- R17. Desfazer e refazer (plano 001) também voltam mover, redimensionar, setas, alinhar e distribuir.

### Acceptance Examples

- AE1. **Covers R1, R2, R3.** **Given** um card não selecionado, **when** a pessoa clica nele, clica de novo e depois aperta Esc, **then** o card fica selecionado, depois o cursor entra no texto, e por fim o card volta a ficar selecionado.
- AE2. **Covers R5, R6.** **Given** um título dentro de um card dentro de um slide, **when** a pessoa clica no título e aperta Esc duas vezes, **then** a seleção passa do título para o card e do card para o slide, e o caminho na barra acompanha.
- AE3. **Covers R10.** **Given** um card selecionado, **when** a pessoa aperta Shift+seta para a direita, **then** o card anda 10 pixels; **given** o cursor no texto, **when** aperta seta para a direita, **then** só o cursor anda.
- AE4. **Covers R11.** **Given** dois cards lado a lado, **when** a pessoa arrasta um deles e o topo chega perto do topo do outro, **then** aparece uma linha e os topos ficam alinhados; **when** faz o mesmo segurando Alt, **then** não aparece linha e o card para onde o mouse soltar.
- AE5. **Covers R12, R13.** **Given** três cards em alturas diferentes selecionados, **when** a pessoa clica em alinhar pelo topo e depois em distribuir na horizontal, **then** os três ficam com o mesmo topo e o mesmo espaço entre eles.
- AE6. **Covers R9.** **Given** uma caixa de texto com três linhas, **when** a pessoa puxa a alça de baixo para cima até ficar menor que o texto, **then** a caixa para no tamanho do texto.
- AE7. **Covers R16.** **Given** um card movido para a direita no notebook, **when** o arquivo salvo abre num projetor com tela mais larga, **then** o card continua na mesma posição relativa ao slide.

### Scope Boundaries

- Grade fixa na tela fica fora; as guias magnéticas cobrem o alinhamento.
- Girar caixas fica fora.
- Agrupar caixas para mover juntas fica fora; o caminho de caixas permite selecionar a caixa de fora.
- Texto gerado por scripts da página continua não editável, como hoje.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

Este plano cuida só de seleção, mover, redimensionar e alinhar.
A divisão abaixo é o entendimento atual, não um roadmap fechado.

- Barra de formatação e desfazer (`docs/plans/2026-10-17-001-feat-barra-formatacao-plan.md`): este plano depends on a barra fixa e o desfazer de lá. Still to decide: na revisão conjunta, o plano 001 deixa de citar Alt+arrastar (R10 e AE5 de lá).
- Inserir elementos: enables, porque caixas novas usam a mesma seleção, as alças e as guias.
- Gerenciar slides: can proceed independently of este plano; still to decide se o slide inteiro conta como "caixa de fora" para alinhar.

### Dependencies / Assumptions

- O modelo de salvamento atual continua: o editor aplica só as mudanças da pessoa sobre o HTML original.
- Em telas bem mais estreitas que a de edição, a posição proporcional pode deixar caixas um pouco diferentes; isso é aceito.
- A equipe edita num navegador de computador com mouse; toque não é alvo.

### Outstanding Questions

**Deferred to Planning**

- Como guardar posição proporcional em caixas que estão dentro de layouts automáticos da página (linhas e grades do próprio HTML).
- A distância em que a guia magnética começa a grudar.

### Sources / Research

- Rascunhos dos três jeitos de clicar, escolhido o A: https://claude.ai/artifact/8JY3kPhGkcgXPpeTLu1LXp
- Editor atual: `editor.py` (Alt+arrastar com deslocamento em pixels, salvamento por diferenças).
