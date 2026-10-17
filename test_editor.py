"""Salvar duas vezes sem recarregar. Uso: python3 test_editor.py  (precisa de: pip install playwright)

A 1a edição cria uma tag nova; a 2a edita um elemento depois dela. Antes da correção,
o 2o salvamento renumerava o arquivo já salvo e gravava no elemento errado.
"""
import os, shutil, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

here = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
shutil.copy(os.path.join(here, "docs", "slides.html"), tmp)
srv = subprocess.Popen([sys.executable, os.path.join(here, "editor.py"), tmp], env={**os.environ, "PORT": "8797"})
try:
    time.sleep(0.5)
    with sync_playwright() as p:
        pg = p.chromium.launch().new_page()
        pg.goto("http://127.0.0.1:8797/edit/slides.html")
        saved = "document.getElementById('ed-msg').textContent.includes('salvo')"
        pg.evaluate("""() => {
          const e = document.querySelectorAll('[contenteditable]');
          window.first = e[0]; window.last = e[e.length - 1];
          first.innerHTML = '<b>PRIMEIRO</b> ' + first.innerHTML; first.setAttribute('data-edited', '1');
        }""")
        pg.click("#ed-save"); pg.wait_for_function(saved)
        pg.evaluate("() => { document.getElementById('ed-msg').textContent=''; last.textContent='ULTIMO'; last.setAttribute('data-edited','1') }")
        pg.click("#ed-save"); pg.wait_for_function(saved)
        tag = pg.evaluate("() => last.tagName.toLowerCase()")
    src = open(os.path.join(tmp, "slides.html"), encoding="utf-8").read()
    assert "<b>PRIMEIRO</b>" in src, "1a edição sumiu"
    assert f">ULTIMO</{tag}>" in src and src.count("ULTIMO") == 1, "2a edição foi parar no elemento errado"
    assert "data-edid" not in src and "contenteditable" not in src, "marca do editor no arquivo"
    print("ok")
finally:
    srv.terminate(); shutil.rmtree(tmp)
