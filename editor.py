"""Editor visual de HTML. Uso: python editor.py [pasta]  -> http://localhost:8765

Cada tag do HTML original ganha um data-edid. Ao salvar, o navegador manda só as
mudanças (texto, estilo, filhos) e elas são aplicadas ao HTML ORIGINAL,
nunca ao DOM já mexido por scripts. Conteúdo gerado por JS não é editável.
"""
import sys, os, re, html
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "docs")

JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "editor-ui.html"), encoding="utf-8").read()

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
