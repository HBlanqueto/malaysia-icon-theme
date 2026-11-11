#!/usr/bin/env python3
"""Genera los íconos a color: lugares (carpetas), tipos de archivo e íconos de app.

Las figuras vienen de las fuentes simbólicas (src/malaysia-symbolic), así que una carpeta o
un tipo nuevo no necesita dibujo propio: basta con agregar una fila a FOLDERS o MIMETYPES.

Uso:
  python3 tools/color/build.py                 escribe Malaysia/ (claro) y Malaysia-Dark/ (oscuro)
  python3 tools/color/build.py --check         falla si algún archivo está desactualizado
  python3 tools/color/build.py --tint '#e8a33d' --out ~/.local/share/icons/Malaysia-Tinted
                                               escribe un tema tintado con ese acento
                                               (hereda de Malaysia; trae carpetas e íconos de app)
"""
import argparse, colorsys, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SYM = os.path.join(ROOT, "src", "malaysia-symbolic")


def glyph(name):
    """Trazo `d` de una fuente simbólica de un solo path."""
    for ctx in os.listdir(SYM):
        p = os.path.join(SYM, ctx, f"{name}-symbolic.svg")
        if os.path.exists(p):
            ds = re.findall(r' d="([^"]+)"', open(p, encoding="utf-8").read())
            if len(ds) != 1:
                sys.exit(f"{name}-symbolic tiene {len(ds)} paths; usa un trazo propio en EXTRA")
            return ds[0]
    sys.exit(f"no existe src/malaysia-symbolic/*/{name}-symbolic.svg")


# Trazos en rejilla de 16 que todavía no son símbolos del tema.
EXTRA = {
    "note": "M6 12.5V4l7-1.5v8.5M6 12.5a1.8 1.8 0 1 1-3.6 0a1.8 1.8 0 0 1 3.6 0M13 11a1.8 1.8 0 1 1-3.6 0a1.8 1.8 0 0 1 3.6 0",
    "lines": "M4.5 4.5h7M4.5 7h7M4.5 9.5h7M4.5 12h4",
    "box": "M2.5 5 8 2.5 13.5 5v6L8 13.5 2.5 11zM2.5 5 8 7.5 13.5 5M8 7.5v6",
    "sheet": "M2.5 3.5h11v9h-11zM2.5 6.5h11M2.5 9.5h11M6.5 3.5v9",
    "easel": "M2.5 3.5h11v7h-11zM8 10.5v3M5.5 13.5h5",
    "letter-a": "M4 13 8 3l4 10M5.5 9.5h5",
    "puzzle": "M3 5.5h2.5a1.5 1.5 0 1 1 3 0H11v2.5a1.5 1.5 0 1 1 0 3V13H3z",
    "terminal": "M3.5 5l3 3-3 3M8 11.5h4.5",
    "chip": "M4.5 4.5h7v7h-7zM6.5 2.5v2M9.5 2.5v2M6.5 11.5v2M9.5 11.5v2M2.5 6.5h2M2.5 9.5h2M11.5 6.5h2M11.5 9.5h2",
    "apps": "M3 3h4v4H3zM9 3h4v4H9zM3 9h4v4H3zM9 9h4v4H9z",
    "symlink": "M3.5 12.5v-3a3 3 0 0 1 3-3h6M9.5 3.5l3 3-3 3",
    "shapes": "M6 8.5a3 3 0 1 0 0-6a3 3 0 0 0 0 6M8.5 8.5h5v5h-5z",
    "eye": "M1.5 8s2.5-4.5 6.5-4.5S14.5 8 14.5 8s-2.5 4.5-6.5 4.5S1.5 8 1.5 8zM8 10a2 2 0 1 0 0-4a2 2 0 0 0 0 4",
}
G = lambda n: EXTRA[n] if n in EXTRA else glyph(n)

# nombre → figura (None = carpeta lisa)
FOLDERS = {
    "folder": None, "inode-directory": None, "folder-drag-accept": "open",
    "folder-documents": "text-x-generic", "folder-download": "arrow-down", "folder-music": "note",
    "folder-pictures": "photo", "folder-videos": "video-x-generic", "folder-projects": "text-x-script",
    "folder-publicshare": "avatar-default", "folder-remote": "network-workgroup",
    "folder-templates": "edit-copy", "user-desktop": "video-display", "user-home": "go-home",
    "user-bookmarks": "user-bookmarks",
}
# nombre → (figura, color de la etiqueta, texto de la etiqueta)
MIMETYPES = {
    "application-certificate": ("system-lock-screen", "#b07d12", "CERT"),
    "application-x-addon": ("puzzle", "#6b4fd8", "ADDON"),
    "application-x-executable": ("terminal", "#2a2d33", "EXEC"),
    "application-x-firmware": ("chip", "#5f6570", "FW"),
    "application-x-generic": ("apps", "#1e7bf2", "APP"),
    "application-x-sharedlib": ("chip", "#5f6570", "LIB"),
    "audio-x-generic": ("note", "#e2306e", "AUDIO"),
    "font-x-generic": ("letter-a", "#5f6570", "FONT"),
    "image-x-generic": ("photo", "#0f97bd", "IMAGE"),
    "inode-symlink": ("symlink", "#7a808a", "LINK"),
    "model": ("box", "#e0632a", "3D"),
    "package-x-generic": ("box", "#b07d12", "PKG"),
    "text-html": ("network-workgroup", "#e0632a", "HTML"),
    "text-x-generic": ("lines", "#6b7280", "TXT"),
    "text-x-preview": ("eye", "#6b7280", "TXT"),
    "text-x-script": ("text-x-script", "#2a2d33", "CODE"),
    "video-x-generic": ("media-playback-start", "#6b4fd8", "VIDEO"),
    "x-office-addressbook": ("avatar-default", "#e0632a", "VCF"),
    "x-office-document": ("lines", "#1e6fe0", "DOC"),
    "x-office-document-template": ("lines", "#1e6fe0", "DOT"),
    "x-office-drawing": ("shapes", "#c13fc9", "ODG"),
    "x-office-presentation": ("easel", "#e86a10", "PPT"),
    "x-office-presentation-template": ("easel", "#e86a10", "POT"),
    "x-office-spreadsheet": ("sheet", "#1f9a46", "XLS"),
    "x-office-spreadsheet-template": ("sheet", "#1f9a46", "XLT"),
    "x-package-repository": ("box", "#b07d12", "REPO"),
}
TEMPLATES = {k for k in MIMETYPES if k.endswith("-template")}

# Letras de trazo en una caja de 6 de alto (ancho, trazo). Así la etiqueta no depende de
# las fuentes instaladas: un ícono con <text> se ve distinto en cada sistema.
LETTERS = {
    "A": (4, "M0 6 2 0l2 6M.7 4h2.6"), "B": (3.8, "M0 3h2.3a1.5 1.5 0 0 1 0 3H0V0h2a1.5 1.5 0 0 1 0 3"), "C": (4, "M4 1A2.4 3 0 1 0 4 5"),
    "D": (4, "M0 0v6h1.4A2.6 3 0 0 0 1.4 0z"), "E": (3.6, "M3.6 0H0v6h3.6M0 3h3"),
    "F": (3.6, "M3.6 0H0v6M0 3h3"), "G": (4, "M4 1A2.4 3 0 1 0 4 5V3.4H2.4"),
    "H": (4, "M0 0v6M4 0v6M0 3h4"), "I": (0, "M0 0v6"), "K": (4, "M0 0v6M4 0 0 3.8M1.5 2.6 4 6"),
    "L": (3.4, "M0 0v6h3.4"), "M": (5, "M0 6V0l2.5 4L5 0v6"), "N": (4, "M0 6V0l4 6V0"),
    "O": (4, "M2 0A2 3 0 1 0 2 6A2 3 0 1 0 2 0z"), "P": (3.8, "M0 6V0h2.2a1.6 1.6 0 0 1 0 3.2H0"),
    "R": (3.8, "M0 6V0h2.2a1.6 1.6 0 0 1 0 3.2H0M2.2 3.2 3.8 6"),
    "S": (3.8, "M3.6.9C3.2.3 2.7 0 1.9 0 .9 0 .2.6.2 1.5c0 2 3.6 1.1 3.6 3 0 .9-.8 1.5-1.9 1.5-.9 0-1.6-.4-1.9-1"),
    "T": (4, "M0 0h4M2 0v6"), "U": (4, "M0 0v4a2 2 0 0 0 4 0V0"), "V": (4, "M0 0l2 6 2-6"),
    "W": (5.4, "M0 0l1.3 6L2.7 1.8 4.1 6 5.4 0"), "X": (4, "M0 0l4 6M4 0 0 6"),
    "3": (3.6, "M.2 0h3.2L1.6 2.4h.4a1.8 1.8 0 1 1-1.8 2.6"),
}


def label(text, cx, top, height, color):
    s, gap = height / 6, 1.25
    widths = [LETTERS[c][0] for c in text]
    total = (sum(widths) + gap * (len(text) - 1)) * s
    x, out = cx - total / 2, []
    for c, w in zip(text, widths):
        out.append(f'<path transform="translate({x:.2f} {top}) scale({s:.4f})" d="{LETTERS[c][1]}"/>')
        x += (w + gap) * s
    return (f'<g fill="none" stroke="{color}" stroke-width="{1.05 / s:.3f}" stroke-linecap="round" '
            f'stroke-linejoin="round">' + "".join(out) + "</g>")


def shade(hex_, pct):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    f = pct / 100
    ch = lambda v: round(min(255, max(0, v * (1 + f) if f < 0 else v + (255 - v) * f)))
    return "#" + "".join(f"{ch(v):02x}" for v in (r, g, b))


def palette(variant, tint=None):
    if variant == "light":
        return dict(back=("#58a6ee", "#2f7fd6"), front=("#9ad2fb", "#5fb0f2"), glyph="#1f62ad",
                    rim="#0a326e", rim_a=.28, hi=.65)
    if variant == "dark":
        return dict(back=("#2d6fbf", "#1c4f8e"), front=("#5b9fe3", "#3a7ecb"), glyph="#123b6c",
                    rim="#000000", rim_a=.45, hi=.35)
    # tintado: mismo brillo que el oscuro, con el tono del acento
    h, l, s = colorsys.rgb_to_hls(*(int(tint[i:i + 2], 16) / 255 for i in (1, 3, 5)))
    def hls(l2, s2):
        return "#" + "".join(f"{round(v * 255):02x}" for v in colorsys.hls_to_rgb(h, l2, min(1, s2)))
    return dict(back=(hls(.46, s * .75), hls(.34, s * .75)), front=(hls(.66, s * .85), hls(.52, s * .85)),
                glyph=hls(.22, s * .8), rim="#000000", rim_a=.45, hi=.35)


def svg(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 64 64">'
            + (f"<defs>{defs}</defs>" if defs else "") + body + "</svg>\n")


def grad(id_, a, b):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')


def emboss(d, x, y, k, color, alpha):
    common = f'fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="{d}"'
    return (f'<g transform="translate({x} {y}) scale({k})">'
            f'<path stroke="#ffffff" stroke-opacity=".45" transform="translate(0 .5)" {common}/>'
            f'<path stroke="{color}" stroke-opacity="{alpha}" {common}/></g>')


def folder(fig, p):
    defs = grad("back", *p["back"]) + grad("front", *p["front"])
    back = '<path fill="url(#back)" d="M5 15a4 4 0 0 1 4-4h14.5l5 5H55a4 4 0 0 1 4 4v28a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/>'
    rim = f'stroke="{p["rim"]}" stroke-opacity="{p["rim_a"]}" stroke-width=".8"'
    if fig == "open":  # carpeta abierta: la tapa se inclina hacia adelante
        front = (f'<path fill="url(#front)" {rim} d="M11.2 24h46.9a3 3 0 0 1 2.9 3.7l-4.6 20.5A4.5 4.5 0 0 1 52 52H9'
                 f'a3.6 3.6 0 0 1-3.5-4.4l4.4-20.8A3.6 3.6 0 0 1 11.2 24z"/>'
                 f'<path d="M11.4 25h46.3" stroke="#ffffff" stroke-opacity="{p["hi"]}" stroke-width=".9" stroke-linecap="round"/>')
        return svg(back + front, defs)
    front = (f'<path fill="url(#front)" {rim} d="M5 23a4 4 0 0 1 4-4h46a4 4 0 0 1 4 4v25a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/>'
             f'<path d="M9 19.9h46" stroke="#ffffff" stroke-opacity="{p["hi"]}" stroke-width=".9" stroke-linecap="round"/>')
    return svg(back + front + (emboss(G(fig), 22, 25.5, 1.25, p["glyph"], .75) if fig else ""), defs)


def document(fig, color, text, template):
    defs = grad("page", "#ffffff", "#eef0f4")
    edge = 'stroke="#141e32" stroke-opacity=".22" stroke-width=".8"'
    dash = ' stroke-dasharray="2.2 1.6"' if template else ""
    body = (f'<path fill="url(#page)" {edge}{dash} d="M15 5h22l13 13v39a2 2 0 0 1-2 2H15a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/>'
            f'<path fill="#e3e6ec" {edge} stroke-linejoin="round" d="M37 5v11a2 2 0 0 0 2 2h11"/>'
            f'<g transform="translate(22.5 20) scale(1.19)"><path fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" d="{G(fig)}"/></g>'
            f'<rect x="13" y="44" width="37" height="11" rx="2" fill="{color}"/>'
            f'<rect x="13" y="44" width="37" height="5.5" rx="2" fill="#ffffff" fill-opacity=".14"/>'
            + label(text, 31.5, 47, 5, "#ffffff"))
    return svg(body, defs)


# ---------------------------------------------------------------- íconos de app (fase 4)
# Squircle de esquina continua (superelipse, n = 5). Área útil de 824 de 1024, como la
# plantilla de app de macOS: 80.47 de 100 unidades, centrada.
SQ_HALF, SQ_N = 40.23, 5


def squircle(half=SQ_HALF, n=SQ_N, steps=180):
    import math
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        c, s_ = math.cos(t), math.sin(t)
        x = 50 + half * math.copysign(abs(c) ** (2 / n), c)
        y = 50 + half * math.copysign(abs(s_) ** (2 / n), s_)
        pts.append(f"{x:.2f} {y:.2f}")
    return "M" + "L".join(pts) + "z"


def gear(teeth=8, outer=6.3, root=4.7, hole=2.2):
    import math
    pts = []
    for k in range(teeth):
        a, w = 2 * math.pi * k / teeth - math.pi / 2, math.pi / teeth * 0.55
        for t, r in ((a - w * 1.25, root), (a - w * .75, outer), (a + w * .75, outer), (a + w * 1.25, root)):
            pts.append(f"{8 + r * math.cos(t):.2f} {8 + r * math.sin(t):.2f}")
    return "M" + "L".join(pts) + f"zM8 {8 + hole}a{hole} {hole} 0 1 0 0-{2 * hole}a{hole} {hole} 0 0 0 0 {2 * hole}"


# id → (figura en rejilla de 16, degradado del fondo en claro arriba/abajo)
APPS = {
    "io.github.hblanqueto.malaysia.settings": (gear(), ("#80858d", "#4f545b")),
    "io.github.hblanqueto.malaysia.screenshot": (
        "M2.5 5.5v-2a1 1 0 0 1 1-1h2M10.5 2.5h2a1 1 0 0 1 1 1v2M13.5 10.5v2a1 1 0 0 1-1 1h-2"
        "M5.5 13.5h-2a1 1 0 0 1-1-1v-2M8 10a2 2 0 1 0 0-4a2 2 0 0 0 0 4", ("#62739a", "#2b3449")),
}
MIN_CONTRAST = 3.0  # WCAG 2.2, 1.4.11: contraste mínimo de un objeto gráfico


def luminance(hex_):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    r, g, b = (ch(int(hex_[i:i + 2], 16)) for i in (1, 3, 5))
    return .2126 * r + .7152 * g + .0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + .05) / (lb + .05)


def app_layers(colors, variant, tint=None):
    """Colores de las tres capas (fondo, figura, borde) para cada modo."""
    top, bottom = colors
    if variant == "light":
        return dict(bg=(top, bottom), fig=("#ffffff", "#e9edf2"), rim=.45)
    if variant == "dark":
        return dict(bg=("#34373d", "#17181b"), fig=(shade(top, 45), shade(top, 20)), rim=.14)
    # el acento lo elige el usuario: si la figura no llega al contraste mínimo, se aclara
    bg = (shade(tint, -62), shade(tint, -78))
    for lift in range(5, 101, 5):
        fig = (shade(tint, min(100, lift + 20)), shade(tint, lift))
        if min(contrast(f, b) for f in fig for b in bg) >= MIN_CONTRAST:
            break
    return dict(bg=bg, fig=fig, rim=.14)


def app_icon(fig, colors, variant, tint=None, name=""):
    L = app_layers(colors, variant, tint)
    worst = min(contrast(f, b) for f in L["fig"] for b in L["bg"])
    if worst < MIN_CONTRAST:
        sys.exit(f"{name} ({variant}): contraste figura/fondo {worst:.2f}:1, mínimo {MIN_CONTRAST}:1")
    sq = squircle()
    defs = (grad("bg", *L["bg"]) + grad("fig", *L["fig"])
            + f'<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" '
              f'stop-opacity="{L["rim"]}"/><stop offset=".35" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
            + f'<clipPath id="sq"><path d="{sq}"/></clipPath>')
    common = 'fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    body = (
        # 1. fondo
        f'<path fill="url(#bg)" d="{sq}"/>'
        # 2. figura: sombra corta debajo y figura con degradado
        f'<g transform="translate(24.4 25.2) scale(3.2)"><path {common} stroke="#000000" stroke-opacity=".18" d="{fig}"/></g>'
        f'<g transform="translate(24.4 24.4) scale(3.2)"><path {common} stroke="url(#fig)" d="{fig}"/></g>'
        # 3. borde: luz interior arriba y contorno exterior (Golden Gate)
        f'<path clip-path="url(#sq)" fill="none" stroke="url(#rim)" stroke-width="2.4" d="{sq}"/>'
        f'<path fill="none" stroke="#000000" stroke-opacity=".18" stroke-width=".6" d="{sq}"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 100 100">'
            f"<defs>{defs}</defs>{body}</svg>\n")


CONTEXTS = {"apps": "Applications", "places": "Places", "mimetypes": "MimeTypes", "status": "Status"}
# scalable/status solo lleva folder-open, que meson instala como enlace a places/folder.svg
VARIANT_DIRS = ["scalable/apps", "scalable/mimetypes", "scalable/places", "scalable/status"]


def theme_index(name, comment, inherits, dirs):
    s = (f"[Icon Theme]\nName={name}\nComment={comment}\nExample=folder\nInherits={inherits}\n\n"
         f"Directories={','.join(dirs)}\n")
    for d in dirs:
        s += f"\n[{d}]\nContext={CONTEXTS[d.split('/')[1]]}\nSize=128\nMinSize=8\nMaxSize=512\nType=Scalable\n"
    return s


def files(variant, tint=None):
    p = palette(variant, tint)
    out = {}
    for name, fig in FOLDERS.items():
        ctx = "mimetypes" if name.startswith("inode-") else "places"
        out[f"scalable/{ctx}/{name}.svg"] = folder(fig, p)
    for name, (fig, colors) in APPS.items():
        out[f"scalable/apps/{name}.svg"] = app_icon(fig, colors, variant, tint, name)
    if variant == "light":
        for name, (fig, color, text) in MIMETYPES.items():
            out[f"scalable/mimetypes/{name}.svg"] = document(fig, color, text, name in TEMPLATES)
    return out


def sync(base, wanted, check, index=None):
    stale = []
    if index:
        wanted = {**wanted, "index.theme": index}
    for rel, content in wanted.items():
        p = os.path.join(base, rel)
        if not os.path.exists(p) or open(p, encoding="utf-8").read() != content:
            stale.append(os.path.relpath(p, ROOT) if p.startswith(ROOT) else p)
            if not check:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "w", encoding="utf-8").write(content)
    return stale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--tint")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.tint:
        if not (a.out and re.fullmatch(r"#[0-9a-fA-F]{6}", a.tint)):
            sys.exit("--tint necesita un color #rrggbb y --out")
        out = os.path.expanduser(a.out)
        sync(out, files("tinted", a.tint.lower()), False,
             theme_index(os.path.basename(out.rstrip("/")), f"Malaysia folders tinted {a.tint}", "Malaysia",
                         VARIANT_DIRS))
        os.makedirs(os.path.join(out, "scalable", "status"), exist_ok=True)
        link = os.path.join(out, "scalable", "status", "folder-open.svg")
        if not os.path.lexists(link):
            os.symlink("../places/folder.svg", link)
        print(f"tema tintado escrito en {out}")
        return
    stale = sync(os.path.join(ROOT, "Malaysia"), files("light"), a.check)
    stale += sync(os.path.join(ROOT, "Malaysia-Dark"), files("dark"), a.check,
                  theme_index("Malaysia-Dark", "Malaysia with dark folders and app icons", "Malaysia",
                              VARIANT_DIRS))
    if a.check:
        sys.exit("desactualizados:\n  " + "\n  ".join(stale)) if stale else print("todo al día")
    else:
        print(f"{len(stale)} archivos escritos")


if __name__ == "__main__":
    main()
