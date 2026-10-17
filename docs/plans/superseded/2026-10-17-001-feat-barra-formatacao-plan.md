---
title: Barra de formatacao e desfazer - Plan
type: feat
date: 2026-10-17
topic: barra-formatacao
artifact_contract: ce-unified-plan/v1
artifact_readiness: requirements-only
product_contract_source: ce-brainstorm
execution: code
---

# Barra de formatacao e desfazer - Plan

## Goal Capsule

- **Objetivo:** dar ao editor visual (`editor.py`) uma barra fixa no topo com fonte, tamanho, negrito, itálico, alinhamento, desfazer e refazer.
- **Autoridade de produto:** decisões tomadas com o usuário nesta brainstorm. Inserir elementos, redimensionar e alinhar, e gerenciar slides não fazem parte deste plano; cada um terá um plano próprio.
- **Bloqueios em aberto:** nenhum.

---

## Product Contract

### Summary

Uma barra fixa no topo do editor reúne formatação de texto e desfazer/refazer.
A formatação vale para as palavras selecionadas e, sem seleção, para o bloco inteiro.
O arquivo salvo continua um HTML autocontido que abre igual em qualquer computador.

### Problem Frame

A equipe gera dashboards e apresentações em HTML e precisa ajustá-los sem mexer em código.
O editor atual só edita texto e move elementos com Alt+arrastar; não há como mudar fonte, tamanho ou estilo, nem voltar um erro.
Os arquivos são apresentados em tela cheia no navegador ou enviados por e-mail, então qualquer mudança precisa funcionar sem internet e sem nada externo.

### Key Decisions

- **Barra fixa no topo, não flutuante sobre a seleção.** Os planos seguintes (inserir elementos, redimensionar e alinhar) precisam de botões sempre visíveis, e uma barra fixa evita ter duas barras. A barra só existe no editor; o arquivo apresentado não tem barra. (session-settled: user-approved — chosen over barra flutuante: uma única barra serve a todos os planos seguintes) Governs R1, R2.
- **Só fontes seguras no seletor.** Elas já existem em todo PC, então o arquivo abre igual no e-mail de qualquer pessoa, até sem internet. (session-settled: user-directed — chosen over Google Fonts embutidas ou por link: arquivo autocontido e pequeno) Governs R3, R4.
- **Formatação por palavras selecionadas.** Igual ao PowerPoint e ao Word. (session-settled: user-directed — chosen over só o bloco inteiro: permite destacar uma palavra) Governs R6, R7.
- **Desfazer só enquanto a página está aberta.** O backup `.bak` já cobre o caso de voltar depois de recarregar. (session-settled: user-directed — chosen over histórico que sobrevive ao recarregar: menos trabalho, sem sistema de versões) Governs R11.

### Requirements

**Barra**

- R1. O editor mostra uma barra fixa no topo da tela, com desfazer, refazer e salvar sempre visíveis.
- R2. A barra reúne os controles de fonte, tamanho, negrito, itálico e alinhamento (esquerda, centro, direita).

**Fonte e tamanho**

- R3. O seletor de fonte oferece só fontes seguras, que existem em qualquer computador: Arial, Verdana, Tahoma, Trebuchet MS, Georgia, Times New Roman e Courier New.
- R4. Se o texto selecionado já usa uma fonte fora da lista, o seletor mostra o nome dessa fonte e não a altera até a pessoa escolher outra.
- R5. A pessoa pode trocar o tamanho da letra do que está selecionado.

**Alcance da formatação**

- R6. Fonte, tamanho, negrito e itálico valem para as palavras selecionadas.
- R7. Sem palavras selecionadas, a formatação vale para o bloco de texto onde está o cursor.
- R8. O alinhamento vale sempre para o bloco inteiro, mesmo com palavras selecionadas.

**Desfazer e refazer**

- R9. Desfazer e refazer funcionam pelos botões e por Ctrl+Z e Ctrl+Y.
- R10. Desfazer volta edição de texto, formatação e movimento com Alt+arrastar, na ordem em que aconteceram.
- R11. Salvar não apaga o histórico; recarregar a página apaga.

**Arquivo salvo**

- R12. Toda formatação aplicada aparece no arquivo salvo, inclusive a de bloco inteiro.
- R13. O arquivo salvo continua autocontido, sem marcas do editor e sem nada que dependa de internet.

### Acceptance Examples

- AE1. **Covers R6.** **Given** o título "Resultados do trimestre", **when** a pessoa seleciona só "trimestre" e clica em negrito, **then** só essa palavra fica em negrito.
- AE2. **Covers R7.** **Given** o cursor dentro de um parágrafo sem nada selecionado, **when** a pessoa escolhe Georgia, **then** o parágrafo inteiro passa para Georgia.
- AE3. **Covers R8.** **Given** uma palavra selecionada no meio de um parágrafo, **when** a pessoa clica em centralizar, **then** o parágrafo inteiro fica centralizado.
- AE4. **Covers R4.** **Given** um HTML que usa uma fonte do Google, **when** a pessoa clica nesse texto, **then** o seletor mostra o nome dessa fonte e o texto continua igual.
- AE5. **Covers R10, R11.** **Given** a pessoa moveu um card, salvou e depois deixou um texto em itálico, **when** aperta Ctrl+Z duas vezes, **then** o itálico some e depois o card volta ao lugar, mesmo após o salvamento.
- AE6. **Covers R12, R13.** **Given** um parágrafo formatado inteiro em Verdana, **when** a pessoa salva e abre o arquivo direto no navegador, sem o editor, **then** o parágrafo aparece em Verdana e o arquivo não tem barra nem marca do editor.

### Scope Boundaries

- Cores, bordas, cantos e espaçamento ficam fora; o usuário não os escolheu para este plano.
- Google Fonts, embutidas ou por link, ficam fora.
- Histórico que sobrevive ao recarregar ou ao fechar a página fica fora.
- Texto gerado por scripts da página continua não editável, como hoje.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

Este plano cuida só da barra de formatação e do desfazer.
A divisão abaixo é o entendimento atual, não um roadmap fechado.

- Redimensionar e alinhar: depends on este plano, porque usa a mesma barra para os botões de alinhar e o mesmo desfazer.
- Inserir elementos (caixa de texto, imagem, forma, tabela): depends on este plano, porque os botões de inserir moram na barra fixa.
- Gerenciar slides (criar, duplicar, apagar, reordenar, miniaturas na lateral): shares a barra e o desfazer; still to decide como funciona em páginas com rolagem que não são slides.

### Dependencies / Assumptions

- O modelo de salvamento atual continua: o editor aplica só as mudanças da pessoa sobre o HTML original, sem gravar o que os scripts geraram.
- A equipe edita num navegador de computador; uso pelo celular não é alvo.

### Outstanding Questions

**Deferred to Planning**

- Quais tamanhos o seletor oferece (lista fixa, campo livre ou os dois).
- Como o desfazer convive com o desfazer nativo do navegador ao digitar.

### Sources / Research

- Rascunhos das três posições de barra, escolhida a A: https://claude.ai/artifact/87duU5Qm6skyrJaXLPs6f6
- Editor atual: `editor.py` (edição de texto, Alt+arrastar, salvamento por diferenças).
