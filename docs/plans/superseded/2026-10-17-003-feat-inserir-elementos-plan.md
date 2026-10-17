---
title: Inserir elementos - Plan
type: feat
date: 2026-10-17
topic: inserir-elementos
artifact_contract: ce-unified-plan/v1
artifact_readiness: requirements-only
product_contract_source: ce-brainstorm
execution: code
---

# Inserir elementos - Plan

## Goal Capsule

- **Objetivo:** permitir inserir caixa de texto e imagem pelo editor visual (`editor.py`), e apagar, duplicar, copiar e colar caixas.
- **Autoridade de produto:** decisões tomadas com o usuário nesta brainstorm. Formatação e desfazer (plano 001), seleção e alinhamento (plano 002) e gerenciar slides não fazem parte deste plano.
- **Bloqueios em aberto:** nenhum.

---

## Product Contract

### Summary

A barra fixa ganha botões para inserir caixa de texto e imagem.
As imagens vão dentro do próprio HTML, reduzidas automaticamente para o arquivo caber no e-mail.
Caixas selecionadas podem ser apagadas, duplicadas, copiadas e coladas.

### Problem Frame

Hoje o editor só muda o que já existe no HTML; para acrescentar um texto ou uma imagem a equipe precisa voltar ao código ou gerar o arquivo de novo.
Os arquivos vão por e-mail e precisam abrir sem internet, então uma imagem não pode ficar como link para fora do arquivo.
Fotos de celular passam fácil de 5 MB, e muitos e-mails de empresa barram anexos acima de 10 MB.

### Key Decisions

- **Imagem embutida no HTML e reduzida automaticamente.** Mantém o arquivo autocontido e pequeno o bastante para e-mail. (session-settled: user-directed — chosen over manter original e perguntar a cada vez: arquivo cabe no e-mail sem a pessoa pensar nisso) Governs R4, R5.
- **Só caixa de texto e imagem neste plano.** Formas e tabelas ficam para depois. (session-settled: user-directed — chosen over formas e tabela: escolha do usuário) Governs R1.
- **Apagar sem aviso.** O desfazer traz de volta qualquer caixa apagada, então um aviso só atrapalharia. Governs R10, R14.

### Requirements

**Inserir**

- R1. A barra tem botões para inserir caixa de texto e imagem.
- R2. Uma caixa de texto nova nasce com o texto "Digite aqui" já selecionado para digitar por cima.
- R3. O botão de imagem abre a escolha de arquivo do computador; colar uma imagem com Ctrl+V, sem o cursor num texto, também insere a imagem.
- R4. A imagem fica guardada dentro do HTML, sem link para arquivo de fora.
- R5. Imagens com mais de 1920 pixels de largura são reduzidas para 1920 e comprimidas ao inserir, sem perda visível em tela cheia.

**Onde o item novo entra**

- R6. O item novo entra dentro da caixa selecionada quando ela pode conter outras caixas, como um slide ou um card; se não puder, entra na caixa de fora dela.
- R7. Sem nada selecionado, o item novo entra no slide ou na seção que está no meio da tela.
- R8. O item novo aparece centralizado nessa caixa, por cima dos outros, e já selecionado para mover e redimensionar como no plano 002.

**Apagar, duplicar, copiar e colar**

- R9. Delete ou Backspace apaga as caixas selecionadas, inclusive as que vieram no HTML original; com o cursor no texto, as teclas apagam letras.
- R10. Apagar não pede confirmação.
- R11. Ctrl+D duplica as caixas selecionadas, e a cópia aparece um pouco deslocada da original.
- R12. Ctrl+C e Ctrl+V copiam e colam caixas dentro do mesmo arquivo; a colagem segue a regra de onde o item novo entra (R6, R7).

**Arquivo salvo e desfazer**

- R13. Itens inseridos, apagados, duplicados e colados aparecem no arquivo salvo, que continua autocontido e sem marcas do editor.
- R14. Desfazer e refazer (plano 001) também voltam inserir, apagar, duplicar e colar.

### Acceptance Examples

- AE1. **Covers R2, R8.** **Given** um slide selecionado, **when** a pessoa clica em inserir caixa de texto e digita "Meta 2027", **then** aparece uma caixa no centro do slide com "Meta 2027", selecionada.
- AE2. **Covers R3, R4, R5.** **Given** uma foto de 4000 pixels de largura e 5 MB, **when** a pessoa a insere, **then** a imagem aparece com 1920 pixels de largura no máximo e o arquivo salvo cresce bem menos que 5 MB.
- AE3. **Covers R6.** **Given** um título selecionado dentro de um card, **when** a pessoa insere uma imagem, **then** a imagem entra no card, não dentro do título.
- AE4. **Covers R7.** **Given** nada selecionado e a página rolada até o terceiro slide, **when** a pessoa insere uma caixa de texto, **then** ela aparece no centro do terceiro slide.
- AE5. **Covers R9, R10, R14.** **Given** um card original selecionado, **when** a pessoa aperta Delete e depois Ctrl+Z, **then** o card some sem aviso e volta no mesmo lugar.
- AE6. **Covers R9.** **Given** o cursor no meio de um texto, **when** a pessoa aperta Backspace, **then** só uma letra é apagada.
- AE7. **Covers R12.** **Given** um card copiado com Ctrl+C no slide 1, **when** a pessoa seleciona o slide 2 e aperta Ctrl+V, **then** a cópia do card entra no slide 2.

### Scope Boundaries

- Formas (retângulo, círculo, linha, seta) e tabelas ficam fora.
- Trocar uma imagem existente por outra fica fora; dá para apagar e inserir de novo.
- Copiar e colar entre arquivos diferentes fica fora.
- Imagem por link da internet fica fora, porque quebra o arquivo autocontido.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

Este plano cuida só de inserir, apagar, duplicar, copiar e colar.
A divisão abaixo é o entendimento atual, não um roadmap fechado.

- Barra de formatação e desfazer (`docs/plans/2026-10-17-001-feat-barra-formatacao-plan.md`): depends on a barra fixa, onde moram os botões de inserir, e no desfazer.
- Seleção, redimensionar e alinhar (`docs/plans/2026-10-17-002-feat-selecao-redimensionar-alinhar-plan.md`): depends on a seleção de caixas; itens novos usam as mesmas alças e guias.
- Gerenciar slides: shares a regra de "slide no meio da tela" (R7); still to decide se duplicar slide reaproveita o duplicar deste plano.

### Dependencies / Assumptions

- O modelo de salvamento atual continua: o editor aplica só as mudanças da pessoa sobre o HTML original, agora incluindo itens novos e apagados.
- Apagar uma caixa original pode quebrar um script da página que dependia dela; isso é aceito, porque o desfazer recupera.

### Outstanding Questions

**Deferred to Planning**

- Formato e qualidade da compressão de imagem (por exemplo, manter PNG com transparência e comprimir fotos).
- Como reconhecer "caixa que pode conter outras" num HTML qualquer.

### Sources / Research

- Editor atual: `editor.py` (salvamento por diferenças sobre o HTML original).
