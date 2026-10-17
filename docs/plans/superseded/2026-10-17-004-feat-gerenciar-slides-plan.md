---
title: Gerenciar slides - Plan
type: feat
date: 2026-10-17
topic: gerenciar-slides
artifact_contract: ce-unified-plan/v1
artifact_readiness: requirements-only
product_contract_source: ce-brainstorm
execution: code
---

# Gerenciar slides - Plan

## Goal Capsule

- **Objetivo:** dar ao editor visual (`editor.py`) um painel lateral de miniaturas para criar, duplicar, apagar e reordenar slides, e também seções de páginas com rolagem.
- **Autoridade de produto:** decisões tomadas com o usuário nesta brainstorm. Formatação e desfazer (plano 001), seleção e alinhamento (plano 002) e inserir elementos (plano 003) não fazem parte deste plano.
- **Bloqueios em aberto:** nenhum.

---

## Product Contract

### Summary

Um painel de miniaturas na lateral esquerda mostra cada slide, ou cada seção grande de uma página com rolagem.
Pelo painel a pessoa cria, duplica, apaga e reordena slides arrastando as miniaturas.
Um slide novo copia o estilo do slide atual e nasce vazio, com um título para editar.

### Problem Frame

Os HTMLs da equipe variam de apresentações em slides a páginas longas com rolagem.
Hoje mudar a ordem, repetir ou tirar um slide exige mexer no código.
Sem uma visão geral, a pessoa precisa rolar o arquivo inteiro para achar onde está.

### Key Decisions

- **O painel também vale para páginas com rolagem.** Cada seção grande vira uma miniatura e recebe as mesmas ações dos slides. (session-settled: user-directed — chosen over painel só em apresentações: os formatos da equipe variam e reordenar seções é útil nos dois) Governs R1, R2.
- **Slide novo copia o estilo do atual.** Mantém o visual do arquivo sem a pessoa escolher nada. (session-settled: user-directed — chosen over menu de layouts e slide em branco: menos passos, visual consistente) Governs R6.
- **Painel na lateral esquerda.** O topo já é da barra fixa (plano 001). Governs R3.
- **Copiar um slide não copia identificadores únicos.** A página não quebra, mesmo que um gráfico feito por script não apareça na cópia. Governs R8.

### Requirements

**Painel**

- R1. O editor reconhece como slide cada bloco grande que se repete no primeiro nível da página, como seções de uma apresentação ou partes de uma página com rolagem.
- R2. Com dois ou mais slides reconhecidos, aparece um painel de miniaturas; com um só, o painel não aparece.
- R3. O painel fica na lateral esquerda e pode ser recolhido para dar espaço à página.
- R4. As miniaturas mostram a aparência atual de cada slide e se atualizam depois de cada edição.
- R5. Clicar numa miniatura leva a página até aquele slide e o marca como slide atual.

**Ações**

- R6. O botão de slide novo cria, logo depois do slide atual, um slide com o mesmo estilo dele, vazio e com um título "Novo slide" pronto para editar.
- R7. Ctrl+D com uma miniatura selecionada, ou o botão de duplicar, cria uma cópia do slide logo depois dele.
- R8. A cópia de um slide não repete identificadores únicos do original, para não quebrar scripts da página.
- R9. Delete com uma miniatura selecionada, ou o botão de apagar, apaga o slide sem pedir confirmação; o último slide restante não pode ser apagado.
- R10. Arrastar uma miniatura para outra posição reordena os slides na página.

**Arquivo salvo e desfazer**

- R11. Slides novos, duplicados, apagados e reordenados aparecem no arquivo salvo, que continua autocontido e sem marcas do editor.
- R12. Desfazer e refazer (plano 001) também voltam criar, duplicar, apagar e reordenar slides.

### Acceptance Examples

- AE1. **Covers R1, R2.** **Given** uma página com rolagem feita de quatro seções, **when** ela abre no editor, **then** o painel mostra quatro miniaturas; **given** uma página de um bloco só, **then** o painel não aparece.
- AE2. **Covers R6.** **Given** o slide 2 com fundo azul como atual, **when** a pessoa clica em slide novo, **then** surge um slide 3 com fundo azul, vazio, com "Novo slide" no título, e os antigos 3 em diante descem uma posição.
- AE3. **Covers R7, R8.** **Given** um slide com um gráfico gerado por script, **when** a pessoa o duplica, **then** a cópia aparece logo depois, o gráfico original continua funcionando e a área do gráfico na cópia pode ficar vazia.
- AE4. **Covers R9, R12.** **Given** três slides, **when** a pessoa apaga o slide 2 e aperta Ctrl+Z, **then** o slide some sem aviso e volta na mesma posição; **given** um slide só, **then** o apagar fica desativado.
- AE5. **Covers R10, R11.** **Given** cinco slides, **when** a pessoa arrasta a miniatura do slide 5 para o topo e salva, **then** o arquivo salvo abre com aquele slide primeiro.

### Scope Boundaries

- Menu de layouts de slide fica fora; o slide novo sempre copia o estilo do atual.
- Navegação de apresentação (setas para trocar de slide, modo apresentador) fica fora; o editor não muda como o arquivo é apresentado.
- Transições e animações entre slides ficam fora.
- Mover slides entre arquivos diferentes fica fora.

<!-- ce-section: work-relationships -->
### How This Work Fits Together

Este plano cuida só do painel de miniaturas e das ações sobre slides.
A divisão abaixo é o entendimento atual, não um roadmap fechado.

- Barra de formatação e desfazer (`docs/plans/2026-10-17-001-feat-barra-formatacao-plan.md`): depends on o desfazer e a barra fixa, onde ficam os botões de slide novo, duplicar e apagar.
- Seleção, redimensionar e alinhar (`docs/plans/2026-10-17-002-feat-selecao-redimensionar-alinhar-plan.md`): shares a ideia de "caixa de fora"; still to decide se o slide é o limite para alinhar caixas sozinhas.
- Inserir elementos (`docs/plans/2026-10-17-003-feat-inserir-elementos-plan.md`): shares Ctrl+D e Delete; o atalho age sobre o slide quando a seleção está numa miniatura e sobre a caixa quando está na página.

### Dependencies / Assumptions

- O modelo de salvamento atual continua: o editor aplica só as mudanças da pessoa sobre o HTML original, agora incluindo blocos novos, apagados e reordenados.
- Scripts da página que contam ou numeram slides podem não perceber slides novos até o arquivo ser reaberto; isso é aceito.

### Outstanding Questions

**Deferred to Planning**

- A regra exata para reconhecer "bloco grande que se repete no primeiro nível" num HTML qualquer.
- Como desenhar as miniaturas sem pesar o editor em arquivos com muitos slides.
