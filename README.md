# html-editor

Editor visual de HTML em Python puro (só stdlib). Abre qualquer HTML autocontido, edita texto e posições no navegador e salva de volta no mesmo arquivo.

    python3 editor.py [pasta]     # padrão: ./docs  ->  http://localhost:8765

- Clique no texto para editar.
- Alt+arrastar move um elemento (Alt+Shift move o bloco pai).
- Salvar grava só as suas mudanças no HTML original (backup em `.bak`). Conteúdo gerado por JS não é editável.

`docs/` tem dois HTMLs fictícios para teste.
