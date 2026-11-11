#!/usr/bin/env python3
"""Generate docs/propuesta-malaysia-icons.html.

Usage: python3 tools/proposal/build.py <malaysia-path> <barrierkit-path>
"""
import base64, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
NEUTRAL = re.compile(r'(fill|stroke)="#(2e3436|2e3434|474747|222|222222|2d3336|000|000000)"', re.I)

inv = json.loads(subprocess.run([sys.executable, f"{HERE}/inventory.py", *sys.argv[1:3]], capture_output=True, text=True, check=True).stdout)

def theme_art(name, loc, uid):
    if not loc:
        return ""
    size, ctx = loc.split("/")
    ext = "png" if size == "16x16" else "svg"
    p = f"{ROOT}/Malaysia/{loc}/{name}.{ext}"
    raw = open(os.path.realpath(p), "rb").read()
    if size == "symbolic":
        s = re.sub(r"<\?xml[^>]*\?>", "", raw.decode())
        s = NEUTRAL.sub(r'\1="currentColor"', s)
        for i in set(re.findall(r'id="([^"]+)"', s)):
            s = s.replace(f'id="{i}"', f'id="{uid}{i}"').replace(f"#{i})", f"#{uid}{i})")
        return s
    return f'<img alt="" src="data:image/svg+xml;base64,{base64.b64encode(raw).decode()}">'

for n, it in enumerate(inv["items"]):
    it["cur"] = theme_art(it["name"], it["loc"], f"a{n}")

tpl = open(f"{HERE}/template.html", encoding="utf-8").read()
out = f"{ROOT}/docs/propuesta-malaysia-icons.html"
open(out, "w", encoding="utf-8").write(tpl.replace("/*__INV__*/null", json.dumps(inv, ensure_ascii=False).replace("</", "<\\/")))
print(out, f"{os.path.getsize(out)/1e3:.0f} KB")
