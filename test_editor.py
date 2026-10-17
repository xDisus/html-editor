"""Testes do editor. Uso: python3 test_editor.py  (precisa de: pip install playwright)

Sobe o editor numa pasta temporária com cópias de docs/ e roda um cenário por AE do plano.
"""
import os, re, shutil, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

here = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
for f in ("slides.html", "dash.html"):
    shutil.copy(os.path.join(here, "docs", f), tmp)
srv = subprocess.Popen([sys.executable, os.path.join(here, "editor.py"), tmp],
                       env={**os.environ, "PORT": "8797"}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
SAVED = "document.getElementById('ed-msg').textContent.includes('salvo')"
tests = []
def test(f): tests.append(f); return f

def src(name): return open(os.path.join(tmp, name), encoding="utf-8").read()
def reset(name): shutil.copy(os.path.join(here, "docs", name), os.path.join(tmp, name))
def save(pg):
    pg.evaluate("document.getElementById('ed-msg').textContent=''")
    pg.click("#ed-save"); pg.wait_for_function(SAVED)
def center(pg, sel, i=0):
    b = pg.locator(sel).nth(i).bounding_box()
    return b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
def click(pg, sel, i=0, **kw):
    x, y = center(pg, sel, i); pg.mouse.click(x, y, **kw)
def drag(pg, sel, dx, dy, i=0, steps=8):
    x, y = center(pg, sel, i)
    pg.mouse.move(x, y); pg.mouse.down(); pg.mouse.move(x + dx, y + dy, steps=steps); pg.mouse.up()
def top(pg, sel, i=0): return pg.evaluate("([s,i])=>document.querySelectorAll(s)[i].getBoundingClientRect().top", [sel, i])
def no_marks(s): assert not re.search(r"data-ed|contenteditable", s), "marca do editor no arquivo"

@test
def ae1_salvar_duas_vezes(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    pg.evaluate("""() => {
      const e = document.querySelectorAll('[contenteditable]');
      window.first = e[0]; window.last = e[e.length - 1];
      first.innerHTML = '<b>PRIMEIRO</b> ' + first.innerHTML; first.setAttribute('data-edited', '1');
    }""")
    save(pg)
    pg.evaluate("() => { last.textContent='ULTIMO'; last.setAttribute('data-edited','1') }")
    save(pg)
    tag = pg.evaluate("() => last.tagName.toLowerCase()")
    s = src("slides.html")
    assert "<b>PRIMEIRO</b>" in s and f">ULTIMO</{tag}>" in s and s.count("ULTIMO") == 1
    no_marks(s)

@test
def f1_f2_f3_desfazer_texto_e_pilha_sobrevive_ao_salvar(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    click(pg, "h1"); click(pg, "h1")  # 1o seleciona, 2o põe o cursor
    assert pg.evaluate("ed.host()?.tagName") == "H1"
    pg.keyboard.press("End"); pg.keyboard.type("XYZ")
    assert "XYZ" in pg.locator("h1").first.inner_text()
    pg.wait_for_timeout(1200); save(pg)
    assert "XYZ" in src("slides.html")
    pg.keyboard.press("Control+z")
    assert "XYZ" not in pg.locator("h1").first.inner_text(), "Ctrl+Z não desfez a digitação (pilha perdida no salvar?)"
    pg.keyboard.press("Control+y"); assert "XYZ" in pg.locator("h1").first.inner_text()

@test
def f3_f4_filhos_apagar_desfazer_e_script(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/dash.html")
    pg.evaluate("() => ed.act('t', () => { const c=document.getElementById('chart'); ed.touch(c,'kids'); })")
    pg.evaluate("() => ed.act('t', () => { const k=document.querySelector('.k'); ed.touch(k.parentElement,'kids'); k.remove(); })")
    save(pg)
    s = src("dash.html")
    assert s.count('class="k"') == 1 and "Receita" not in s, "filho apagado continua no arquivo"
    assert '<div id="chart"></div>' in s, "conteúdo gerado por script foi gravado"
    pg.keyboard.press("Control+z"); save(pg)
    assert src("dash.html").count('class="k"') == 2 and "Receita" in src("dash.html")
    no_marks(src("dash.html"))

@test
def t_formatacao_ae2_ae4_bloco_e_desfazer(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    click(pg, "p"); click(pg, "p")
    pg.evaluate("""() => { const t=document.querySelector('p').firstChild, i=t.data.indexOf('teste');
      getSelection().setBaseAndExtent(t,i,t,i+5) }""")
    pg.click("#ed-b")
    assert pg.evaluate("[...document.querySelectorAll('p [style]')].map(e=>e.textContent+':'+e.style.fontWeight)") == ["teste:bold"]
    pg.keyboard.press("Control+z")
    assert "style" not in pg.evaluate("document.querySelector('p').innerHTML")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); pg.keyboard.press("Escape"); click(pg, "h1"); click(pg, "h1")
    # sem palavras selecionadas: vale para o bloco
    pg.evaluate("getSelection().collapse(document.querySelector('h1').firstChild, 3)")
    pg.select_option("#ed-font", "Georgia"); pg.fill("#ed-size", "30"); pg.press("#ed-size", "Enter")
    st = pg.evaluate("document.querySelector('h1').getAttribute('style')")
    assert "Georgia" in st and "30px" in st, st
    save(pg); assert "Georgia" in src("slides.html"); no_marks(src("slides.html"))
    # AE4: fonte fora da lista aparece no seletor e nada muda
    pg.evaluate("document.querySelector('p').style.fontFamily='Lobster, cursive'")
    pg.keyboard.press("Escape"); pg.keyboard.press("Escape")
    click(pg, "p")
    assert pg.evaluate("document.getElementById('ed-font').selectedOptions[0].textContent") == "Lobster"

@test
def t5_alinhar_texto_ae3(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    click(pg, "p"); click(pg, "p")
    pg.click("[data-al=c]")
    assert pg.evaluate("document.querySelector('p').style.textAlign") == "center"

@test
def s_ae6_esc_e_caminho(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    pg.evaluate("window.scrollTo(0, document.querySelectorAll('body > section')[1].offsetTop)")
    who = "() => (ed.host() ? 'edit:' : '') + (ed.sel[0] ? ed.sel[0].tagName : '-')"
    click(pg, ".card h3");           assert pg.evaluate(who) == "H3"
    assert pg.inner_text("#ed-path") == "section › div.card › h3", pg.inner_text("#ed-path")
    click(pg, ".card h3");           assert pg.evaluate(who) == "edit:H3"
    pg.keyboard.press("Escape");     assert pg.evaluate(who) == "H3"
    pg.keyboard.press("Escape");     assert pg.evaluate(who) == "DIV"
    pg.keyboard.press("Escape");     assert pg.evaluate(who) == "SECTION"
    pg.click("#ed-path span[data-n='0']"); assert pg.evaluate(who) == "SECTION"

@test
def s_ae7_guias_e_alt(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/dash.html")
    drag(pg, ".k", 0, 80, i=1)                # k2 desce 80px
    assert abs(top(pg, ".k", 1) - top(pg, ".k", 0)) > 50
    drag(pg, ".k", 0, -78, i=1, steps=12)     # sobe a 2px do topo do outro
    assert abs(top(pg, ".k", 1) - top(pg, ".k", 0)) < .6, "guia não alinhou os topos"
    drag(pg, ".k", 0, 80, i=1)
    pg.keyboard.down("Alt"); drag(pg, ".k", 0, -78, i=1, steps=12); pg.keyboard.up("Alt")
    assert abs(top(pg, ".k", 1) - top(pg, ".k", 0)) > .6, "Alt devia desligar as guias"

@test
def s_ae5_ae8_setas_alinhar_distribuir_e_ae9(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/dash.html")
    # AE5: mover, italico, desfazer 2x
    drag(pg, ".k", 40, 0)
    x1 = pg.evaluate("document.querySelector('.k').getBoundingClientRect().left")
    pg.evaluate("ed.fmt('italic')")
    pg.keyboard.press("Control+z"); pg.keyboard.press("Control+z")
    assert pg.evaluate("document.querySelector('.k').getBoundingClientRect().left") < x1 - 30
    pg.keyboard.press("Control+y"); pg.keyboard.press("Control+y")
    # setas
    l0 = pg.evaluate("document.querySelector('.k').getBoundingClientRect().left")
    pg.keyboard.press("ArrowRight"); pg.keyboard.press("Shift+ArrowRight")
    assert abs(pg.evaluate("document.querySelector('.k').getBoundingClientRect().left") - l0 - 11) < .6
    # AE8: três caixas, alturas diferentes
    pg.evaluate("""() => { for (const t of ['ca','cb','cc']) {
      const d=document.createElement('div'); d.className='x'; d.textContent=t; d.style.cssText='width:80px;height:40px;background:#ccc';
      document.body.append(d); d.setAttribute('data-edid','9'+t); } }""")
    pg.evaluate("document.querySelectorAll('.x').forEach((d,i)=>{d.style.marginTop=(i*30)+'px'; d.style.marginLeft=[0,150,500][i]+'px'; d.style.width=(50+i*40)+'px'})")
    pg.evaluate("ed.select([...document.querySelectorAll('.x')])")
    pg.click("[data-al=t]"); pg.click("[data-dist=h]")
    r = pg.evaluate("[...document.querySelectorAll('.x')].map(d=>{const r=d.getBoundingClientRect();return [r.top,r.left,r.right]})")
    assert max(a[0] for a in r) - min(a[0] for a in r) < .6, r
    r.sort(key=lambda a: a[1]); g1, g2 = r[1][1] - r[0][2], r[2][1] - r[1][2]
    assert abs(g1 - g2) < .6, (g1, g2)
    # AE9: posição proporcional
    pg.evaluate("ed.select([document.querySelector('.k')])")
    save(pg); s = src("dash.html"); assert "left:" in s.replace(" ", "") and "%" in s
    ratios = []
    for w in (1280, 1920):
        p2 = br.new_page(viewport={"width": w, "height": 800}); p2.goto("file://" + os.path.join(tmp, "dash.html"))
        ratios.append(p2.evaluate("(()=>{const k=document.querySelector('.k').getBoundingClientRect(),r=document.querySelector('.row').getBoundingClientRect();return (k.left-r.left)/r.width})()"))
        p2.close()
    assert abs(ratios[0] - ratios[1]) < .01, ratios

@test
def s_redimensionar_e_card_absoluto(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    pg.evaluate("window.scrollTo(0, document.querySelectorAll('body > section')[1].offsetTop)")
    click(pg, ".card")
    w0 = pg.evaluate("document.querySelector('.card').getBoundingClientRect().width")
    hx, hy = pg.evaluate("(()=>{const h=document.querySelector('#ed-ov [data-h=e]').getBoundingClientRect();return [h.x+h.width/2,h.y+h.height/2]})()")
    pg.mouse.move(hx, hy); pg.mouse.down(); pg.mouse.move(hx + 100, hy, steps=6); pg.mouse.up()
    assert abs(pg.evaluate("document.querySelector('.card').getBoundingClientRect().width") - w0 - 100) < 2
    assert "%" in pg.evaluate("document.querySelector('.card').style.width")
    pg.keyboard.press("Control+z")
    assert abs(pg.evaluate("document.querySelector('.card').getBoundingClientRect().width") - w0) < 1

@test
def i_ae10_ae11_ae12_inserir_apagar(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    pg.evaluate("window.scrollTo(0, document.querySelectorAll('body > section')[1].offsetTop)")
    # AE11: título dentro do card selecionado -> imagem entra no card
    click(pg, ".card h3")
    pg.evaluate("""async () => { const c=document.createElement('canvas'); c.width=4000; c.height=2500;
      const x=c.getContext('2d'); for(let i=0;i<40;i++){x.fillStyle=`hsl(${i*9},80%,50%)`;x.fillRect(i*100,0,100,2500)}
      for(let i=0;i<4000;i+=7){x.fillStyle='#'+((i*977)%0xffffff).toString(16).padStart(6,'0');x.fillRect(i,(i*13)%2500,6,6)}
      const b=await new Promise(r=>c.toBlob(r,'image/png')); window.big=b.size; await ed.insertImage(b) }""")
    assert pg.evaluate("document.querySelector('.card > img')?.naturalWidth") == 1920
    save(pg); s = src("slides.html")
    assert "data:image/jpeg" in s and len(s) < pg.evaluate("big") / 2, "imagem não foi reduzida"
    assert '<img src="data:' in s or "<img" in s
    # texto novo entra no slide visível quando nada está selecionado
    pg.evaluate("ed.select([])"); pg.click("#ed-ins-text")
    assert pg.evaluate("ed.sel[0].parentElement === document.querySelectorAll('body > section')[1]")
    # AE12: apagar sem aviso e desfazer
    pg.evaluate("ed.select([document.querySelector('.card')])")
    pg.keyboard.press("Delete")
    assert pg.evaluate("!document.querySelector('body > section .card')")
    save(pg); assert 'class="card"' not in src("slides.html")
    pg.keyboard.press("Control+z"); save(pg)
    assert 'class="card"' in src("slides.html") and "Digite aqui" in src("slides.html")
    no_marks(src("slides.html"))
    # Backspace no texto apaga letra, não a caixa
    pg.evaluate("scrollTo(0,0)"); click(pg, "h1"); click(pg, "h1"); pg.keyboard.press("End"); pg.keyboard.press("Backspace")
    t = pg.locator("h1").first.inner_text(); assert t == "Resultados do trimestr", (t, pg.evaluate("ed.host()?.tagName"), pg.evaluate("ed.sel.map(e=>e.tagName)"))

@test
def i_duplicar_copiar_colar_sem_id(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/dash.html")
    pg.evaluate("document.querySelector('.k').id='orig'")
    click(pg, ".k"); pg.keyboard.press("Control+d")
    assert pg.evaluate("document.querySelectorAll('.k').length") == 3
    assert pg.evaluate("document.querySelectorAll('#orig').length") == 1
    pg.keyboard.press("Control+c"); pg.keyboard.press("Escape")
    pg.evaluate("ed.paste()")
    assert pg.evaluate("document.querySelectorAll('.k').length") == 4
    assert pg.evaluate("[...document.querySelectorAll('.k')].every(k=>k.querySelector('b'))"), "colar perdeu os filhos"
    # id dentro de texto editado sobrevive ao salvar
    pg.evaluate("document.getElementById('t').innerHTML='x <span id=\"nota\">y</span>'; ed.act('t',()=>ed.touch(document.getElementById('t'),'html'))")
    save(pg); s = src("dash.html"); assert 'id="nota"' in s and s.count('class="k"') == 4 and s.count('id="orig"') <= 1; no_marks(s.replace('id="orig"', ""))

@test
def l_ae13_a_ae16_slides(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/dash.html")
    assert pg.evaluate("ed.slides().length") == 0 and pg.is_hidden("#ed-panel")
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    assert pg.evaluate("ed.slides().length") == 2 and pg.is_visible("#ed-panel")
    assert pg.locator("#ed-panel .th").count() == 2
    # AE14: slide novo copia o estilo do atual e entra logo depois
    pg.evaluate("document.querySelectorAll('body > section')[0].style.background='rgb(0, 0, 255)'")
    pg.locator("#ed-panel .th").nth(0).click()
    pg.click("#ed-newslide")
    ss = pg.evaluate("[...document.querySelectorAll('body > section')].map(s=>s.innerText.split('\\n')[0])")
    assert ss == ["Resultados do trimestre", "Novo slide", "Destaques"], ss
    assert pg.evaluate("getComputedStyle(document.querySelectorAll('body > section')[1]).backgroundColor") == "rgb(0, 0, 255)"
    pg.wait_for_timeout(500); assert pg.locator("#ed-panel .th").count() == 3
    # AE16: duplicar slide com card e id; cópia sem id
    pg.evaluate("document.querySelectorAll('body > section')[2].id='orig'; ed.goto(2)")
    pg.click("#ed-dupslide")
    assert pg.evaluate("document.querySelectorAll('body > section').length") == 4 and pg.evaluate("document.querySelectorAll('#orig').length") == 1
    # AE15: mover o último para o topo e salvar
    pg.evaluate("ed.moveSlide(3, 0)"); save(pg)
    s = src("slides.html"); assert s.index("Destaques") < s.index("Resultados do trimestre") < s.index("Novo slide"), "ordem"
    assert s.count("<section") == 4, s.count("<section")
    assert s.count('id="orig"') == 0; no_marks(s.replace('id="orig"', ""))
    # apagar: desfaz e respeita o mínimo
    pg.evaluate("ed.goto(1)"); pg.click("#ed-delslide"); assert pg.evaluate("document.querySelectorAll('body > section').length") == 3
    pg.keyboard.press("Control+z"); assert pg.evaluate("document.querySelectorAll('body > section').length") == 4
    pg.evaluate("[...document.querySelectorAll('body > section')].slice(1).forEach(s=>s.remove())")
    pg.evaluate("ed.delSlide()"); assert pg.evaluate("document.querySelectorAll('body > section').length") == 1

@test
def alinhar_ao_slide_e_painel_com_um_slide(pg, br):
    pg.goto("http://127.0.0.1:8797/edit/slides.html")
    # 2 caixas: alinhar ao slide e distribuir com só 2
    pg.evaluate("ed.select([...document.querySelectorAll('section')[0].children].slice(0,2))")
    pg.select_option("#ed-alignto", "slide")
    assert not pg.is_disabled("[data-dist=v]")
    pg.click("[data-al=l]")
    a = pg.evaluate("[...ed.sel].map(e=>e.getBoundingClientRect().left)")
    sl = pg.evaluate("ed.slides()[0].getBoundingClientRect().left")
    assert all(abs(x - sl) < 1 for x in a), (a, sl)
    # 1 slide só: painel continua lá e dá pra criar outro
    pg.evaluate("[...document.querySelectorAll('body > section')].slice(1).forEach(s=>s.remove())")
    pg.wait_for_selector("#ed-newslide"); pg.click("#ed-newslide")
    assert pg.evaluate("document.querySelectorAll('body > section').length") == 2

try:
    time.sleep(0.6)
    with sync_playwright() as p:
        br = p.chromium.launch()
        fail = 0
        for t in tests:
            for f in ("slides.html", "dash.html"): reset(f)
            pg = br.new_page(viewport={"width": 1280, "height": 800}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            try:
                t(pg, br); assert not errs, errs; print("ok  ", t.__name__)
            except Exception as e:
                fail += 1; import traceback; ln = traceback.extract_tb(e.__traceback__)[-1].lineno
                print("FAIL", t.__name__, "line", ln, "->", str(e)[:300])
            pg.close()
        br.close()
    sys.exit(1 if fail else 0)
finally:
    srv.terminate(); shutil.rmtree(tmp)
