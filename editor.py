"""Editor visual de HTML. Uso: python editor.py [pasta]  -> http://localhost:8765

Cada tag do HTML original ganha um data-edid. Ao salvar, o navegador manda só as
mudanças (texto editado, posição movida) e elas são aplicadas ao HTML ORIGINAL,
nunca ao DOM já mexido por scripts. Conteúdo gerado por JS não é editável.
"""
import sys, os, re, html
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "docs")

JS = r"""
<style data-ed>
[contenteditable]:hover{outline:1px dashed #38f}[contenteditable]:focus{outline:2px solid #38f}
#ed-bar{position:fixed;top:8px;right:8px;z-index:2147483647;background:#222;color:#fff;font:13px sans-serif;padding:8px 12px;border-radius:8px}
#ed-bar button{margin-left:8px}
</style>
<div id="ed-bar" data-ed>Clique = editar texto | Alt+arrastar = mover (Alt+Shift = mover o bloco pai) <button id="ed-save">Salvar</button><span id="ed-msg"></span></div>
<script data-ed>
document.querySelectorAll('body [data-edid]').forEach(e=>{
  if(e.closest('svg,script,style'))return;
  if([...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()))e.setAttribute('contenteditable','true');
});
addEventListener('input',ev=>ev.target.closest('[data-edid]')?.setAttribute('data-edited','1'));
addEventListener('paste',ev=>{ev.preventDefault();document.execCommand('insertText',false,ev.clipboardData.getData('text/plain'))});
addEventListener('click',ev=>{if(ev.target.closest('a')&&!ev.target.closest('[data-ed]'))ev.preventDefault()},true);
let d=null;
addEventListener('pointerdown',ev=>{
  if(!ev.altKey||ev.target.closest('[data-ed]'))return;
  let el=ev.target.closest('[data-edid]');
  if(el&&ev.shiftKey)el=el.parentElement?.closest('[data-edid]')||el;
  if(!el)return;
  ev.preventDefault();
  const m=el.style.transform.match(/translate\((-?[\d.]+)px,\s*(-?[\d.]+)px\)/)||[0,0,0];
  d={el,x:ev.clientX,y:ev.clientY,ox:+m[1],oy:+m[2],base:el.style.transform.replace(/translate\([^)]*\)/,'').trim()};
},true);
addEventListener('pointermove',ev=>{
  if(!d)return;
  d.el.style.transform=(d.base+` translate(${d.ox+ev.clientX-d.x}px, ${d.oy+ev.clientY-d.y}px)`).trim();
  d.el.setAttribute('data-moved','1');
});
addEventListener('pointerup',()=>d=null);
// original numerado UMA vez, ao abrir: os data-edid da página só batem com ele, não com o arquivo já salvo
const raw=fetch(location.pathname.replace('/edit/','/raw/')).then(r=>r.text());
document.getElementById('ed-save').onclick=async()=>{
  const msg=document.getElementById('ed-msg');
  try{
    const doc=new DOMParser().parseFromString(await raw,'text/html');
    const find=e=>doc.querySelector(`[data-edid="${e.dataset.edid}"]`);
    document.querySelectorAll('[data-edited]').forEach(e=>{
      const t=find(e); if(!t)return;
      const c=e.cloneNode(true);
      c.querySelectorAll('*').forEach(x=>['contenteditable','data-edited','data-moved','data-edid'].forEach(a=>x.removeAttribute(a)));
      t.innerHTML=c.innerHTML;
    });
    document.querySelectorAll('[data-moved]').forEach(e=>{
      const t=find(e); if(!t)return;
      const s=e.getAttribute('style'); s?t.setAttribute('style',s):t.removeAttribute('style');
    });
    doc.querySelectorAll('[data-edid]').forEach(e=>e.removeAttribute('data-edid'));
    const r=await fetch(location.pathname.replace('/edit/','/save/'),{method:'POST',body:'<!DOCTYPE html>\n'+doc.documentElement.outerHTML});
    msg.textContent=r.ok?' salvo!':' erro '+r.status;
  }catch(err){msg.textContent=' erro: '+err}
};
</script>
"""

class _Tags(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.starts = [0]
        for line in src.split("\n"):
            self.starts.append(self.starts[-1] + len(line) + 1)
        self.at = []
        self.feed(src)

    def handle_starttag(self, tag, attrs):
        line, col = self.getpos()
        self.at.append(self.starts[line - 1] + col + 1 + len(tag))

def add_ids(src):
    for n, pos in reversed(list(enumerate(_Tags(src).at))):
        src = src[:pos] + f' data-edid="{n}"' + src[pos:]
    return src

def safe(name):
    p = os.path.abspath(os.path.join(ROOT, os.path.basename(unquote(name))))
    return p if p.endswith(".html") and os.path.isfile(p) else None

class H(BaseHTTPRequestHandler):
    def send(self, body, code=200):
        b = body.encode()
        self.send_response(code); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
            return self.send("<h2>Arquivos</h2>" + "".join(f'<p><a href="/edit/{html.escape(f)}">{html.escape(f)}</a></p>' for f in files))
        for kind in ("edit", "raw"):
            if path.startswith(f"/{kind}/") and (p := safe(path[len(kind) + 2:])):
                s = add_ids(open(p, encoding="utf-8").read())
                if kind == "raw":
                    return self.send(s)
                i = s.lower().rfind("</body>")
                return self.send(s[:i] + JS + s[i:] if i >= 0 else s + JS)
        self.send("não achei", 404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith("/save/") and (p := safe(path[6:])):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode()
            os.replace(p, p + ".bak")  # ponytail: um backup só, versionar se precisar
            open(p, "w", encoding="utf-8").write(data)
            return self.send("ok")
        self.send("não achei", 404)

HTTPServer(("127.0.0.1", int(os.environ.get("PORT", 8765))), H).serve_forever()
