#!/usr/bin/env python3
"""Genera docs/icon-map.html: un mockup navegable con todos los íconos del tema.

Uso:  python3 tools/build-icon-map.py
"""
import base64, json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(ROOT, "Adwaita")
OUT = os.path.join(ROOT, "docs", "icon-map.html")

NEUTRAL = re.compile(r'(fill|stroke)="#(2e3436|2e3434|474747|222|222222|2d3336|000|000000)"', re.I)


def clean_symbolic(svg, uid):
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = NEUTRAL.sub(r'\1="currentColor"', svg)
    svg = re.sub(r'\swidth="[^"]*"', "", svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', "", svg, count=1)
    # evitar colisiones de id entre SVG inline
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{uid}-{i}"').replace(f"#{i})", f"#{uid}-{i})").replace(f'"#{i}"', f'"#{uid}-{i}"')
    return svg


icons = []
for size in ("symbolic", "scalable", "16x16"):
    base = os.path.join(THEME, size)
    if not os.path.isdir(base):
        continue
    for ctx in sorted(os.listdir(base)):
        d = os.path.join(base, ctx)
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            name, ext = os.path.splitext(fn)
            link = os.readlink(p) if os.path.islink(p) else None
            item = {"n": name, "s": size, "c": ctx, "b": os.path.getsize(os.path.realpath(p))}
            if link:
                item["l"] = os.path.splitext(link)[0]
            raw = open(os.path.realpath(p), "rb").read()
            if size == "symbolic":
                item["v"] = clean_symbolic(raw.decode("utf-8"), f"i{len(icons)}")
                item["k"] = 1 if re.search(r"#(33d17a|ff7800|e01b24|ed333b)", item["v"], re.I) else 0
            else:
                mime = "image/svg+xml" if ext == ".svg" else "image/png"
                item["u"] = f"data:{mime};base64," + base64.b64encode(raw).decode()
            icons.append(item)

# fuentes en src/
sources = sorted(f.replace(".source.svg", "") for f in os.listdir(os.path.join(ROOT, "src", "fullcolor")))

version = re.search(r"version\s*:\s*'([^']+)'", open(os.path.join(ROOT, "meson.build")).read()).group(1)
data = {"icons": icons, "sources": sources, "version": version}

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon-map.template.html"), encoding="utf-8").read()
html = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
print(f"{len(icons)} íconos -> {OUT} ({os.path.getsize(OUT)/1e6:.1f} MB)")
