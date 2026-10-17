# html-editor

Editor visual de HTML em Python puro (só stdlib). Abre qualquer HTML autocontido, edita no navegador e salva de volta no mesmo arquivo.

    python3 editor.py [pasta]     # padrão: ./docs  ->  http://localhost:8765

- Barra fixa no topo: desfazer/refazer (Ctrl+Z, Ctrl+Y), salvar, fonte, tamanho, negrito, itálico, alinhar, distribuir e inserir (texto, imagem).
- Clique seleciona a caixa; segundo clique põe o cursor no texto; Esc sobe um nível. Shift+clique soma à seleção.
- Arrastar move, alças redimensionam (Shift mantém proporção), setas empurram (Shift = 10 px). Guias magnéticas; Alt desliga.
- Delete apaga, Ctrl+D duplica, Ctrl+C / Ctrl+V copiam e colam (Ctrl+V também cola imagem).
- Painel de slides à esquerda (2+ blocos grandes repetidos): novo, duplicar, apagar, reordenar arrastando.
- Salvar grava só as suas mudanças no HTML original (backup em `.bak`). Conteúdo gerado por JS não é editável nem gravado.
- A interface vive em `editor-ui.html`.

Testes: `pip install playwright && python3 test_editor.py`. `docs/` tem dois HTMLs fictícios.
