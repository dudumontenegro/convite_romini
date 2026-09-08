#!/usr/bin/env python3
"""Gera uma versao unica e autossuficiente do convite (imagens embutidas em base64).
   Uso: python3 build-artifact.py  ->  convite-completo.html"""
import base64, pathlib, re

root = pathlib.Path(__file__).parent
src  = (root / "index.html").read_text()

def datauri(p):
    return "data:image/jpeg;base64," + base64.b64encode((root / p).read_bytes()).decode()

env, card = datauri("assets/envelope.jpg"), datauri("assets/convite.jpg")

# 1 · so o conteudo da pagina (o artifact ja fornece doctype/head/body)
body = src.split("<body>", 1)[1].rsplit("</body>", 1)[0]
head = src.split("<head>", 1)[1].split("</head>", 1)[0]
title = re.search(r"<title>.*?</title>", head, re.S).group(0)
style = re.search(r"<style>.*?</style>", head, re.S).group(0)
gsap  = '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>'

# 2 · as imagens viram custom properties
style = style.replace("*, *::before, *::after { box-sizing: border-box; }",
    f':root {{\n  --img-envelope: url("{env}");\n  --img-convite: url("{card}");\n}}\n'
    "*, *::before, *::after { box-sizing: border-box; }")
body = body.replace('url("assets/envelope.jpg") center / 100% 100% no-repeat',
                    'var(--img-envelope) center / 100% 100% no-repeat')
style = style.replace('url("assets/envelope.jpg") center / 100% 100% no-repeat',
                      'var(--img-envelope) center / 100% 100% no-repeat')
style = style.replace('url("assets/convite.jpg") center / 100% 100% no-repeat',
                      'var(--img-convite) center / 100% 100% no-repeat')

# 3 · o preload passa a ler as proprias custom properties
body = body.replace('''Promise.all([preload("assets/envelope.jpg"), preload("assets/convite.jpg")]).then(() => {''',
'''const cssUrl = (n) => getComputedStyle(document.documentElement)
  .getPropertyValue(n).trim().replace(/^url\\(["']?/, "").replace(/["']?\\)$/, "");

Promise.all([preload(cssUrl("--img-envelope")), preload(cssUrl("--img-convite"))]).then(() => {''')

out = f"{title}\n{style}\n{gsap}\n{body}"
(root / "convite-completo.html").write_text(out)
print(f"convite-completo.html  ·  {len(out)/1024/1024:.2f} MB")
