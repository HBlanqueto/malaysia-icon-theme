#!/usr/bin/env python3
"""Icons for apps the theme does not draw: a plate colored from the app's own SVG.

The plate takes the hue of the darkest lobe of the logo's colors when the logo is light, and of the lightest lobe
when it is dark, so the plate is the logo's own shadow. The other appearances recolor the logo.

Usage:
  python3 tools/color/thirdparty.py /usr/share/icons/hicolor/scalable/apps --appearance dark \\
      --out ~/.local/share/icons/Malaysia-Apps-Dark
  python3 tools/color/thirdparty.py ICON_DIR --appearance tinted --tint '#8a5e1e' --out DIR
Appearances: light, dark, clear, clear-dark, tinted, tinted-dark. Only SVG icons with #rgb or #rrggbb colors are recolored.
"""
import argparse, io, math, os, re, sys
from collections import namedtuple

import resvg_py
from PIL import Image

import appicons, build

Lobe = namedtuple("Lobe", "hue chroma lightness share")
BINS = 24
MIN_SHARE = .15
BRIGHT_LOGO = .6
LOGO_SIDE = .76 * 824  # of the 824 px body
# logo is bright → (plate top, plate bottom, chroma factor, chroma cap) of a dark plate; otherwise a light one
PLATES = {True: (.29, .2, .5, .11), False: (.92, .84, .3, .06)}
HEX = re.compile(r'(?<!url\()(?<!href=")#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
ROOT = re.compile(r"<svg\b([^>]*)>", re.S)
APPEARANCES = ("light", "dark", "clear", "clear-dark", "tinted", "tinted-dark")


def pixels(image):
    """(lightness, chroma, hue) of every mostly opaque pixel."""
    cache = {}
    for r, g, b, alpha in image.get_flattened_data():
        if alpha >= 128:
            cache.setdefault((r, g, b), appicons.rgb_to_oklch(r, g, b))
            yield cache[(r, g, b)]


def lobes(colors):
    """Runs of hue bins that hold chroma, each with its chroma-weighted hue, chroma, lightness and share."""
    colors = [c for c in colors if c[1] >= appicons.NEUTRAL_CHROMA]
    weight = [0.0] * BINS
    for _, chroma, hue in colors:
        weight[int(hue // (360 / BINS)) % BINS] += chroma
    total = sum(weight)
    if total == 0:
        return []
    occupied = [w >= .03 * max(weight) for w in weight]
    gap = occupied.index(False) if False in occupied else -1
    runs, run = [], []
    for i in range(gap + 1, gap + 1 + BINS):
        if occupied[i % BINS]:
            run.append(i % BINS)
        elif run:
            runs.append(run)
            run = []
    runs += [run] if run else []
    found = []
    for run in runs:
        members = [c for c in colors if int(c[2] // (360 / BINS)) % BINS in run]
        w = sum(c[1] for c in members)
        sin = sum(c[1] * math.sin(math.radians(c[2])) for c in members)
        cos = sum(c[1] * math.cos(math.radians(c[2])) for c in members)
        found.append(Lobe(math.degrees(math.atan2(sin, cos)) % 360, sum(c[1] ** 2 for c in members) / w,
                          sum(c[1] * c[0] for c in members) / w, w / total))
    return found


def plate_lobe(colors):
    """(the lobe the plate takes its hue from or None, whether the logo is bright)."""
    bright = sum(c[0] for c in colors) / len(colors) >= BRIGHT_LOGO
    candidates = [lobe for lobe in lobes(colors) if lobe.share >= MIN_SHARE]
    pick = min if bright else max
    return (pick(candidates, key=lambda lobe: lobe.lightness) if candidates else None), bright


def logo_plate(lobe, bright):
    top, bottom, factor, cap = PLATES[bright]
    hue, chroma = (lobe.hue, min(lobe.chroma * factor, cap)) if lobe else (0, 0)
    return appicons.oklch(top, chroma, hue), appicons.oklch(bottom, chroma * .85, hue)


def recolor(text, convert):
    def swap(m):
        hex_ = m[1] if len(m[1]) == 6 else "".join(ch * 2 for ch in m[1])
        return convert(*appicons.to_oklch("#" + hex_))
    return HEX.sub(swap, text)


def converter(appearance, accent):
    """(lightness, chroma, hue) → hex for the appearances that recolor the logo; None keeps its colors."""
    if appearance == "clear":
        return lambda lightness, chroma, hue: appicons.oklch(min(.97, .4 + .52 * lightness), 0, 0)
    if appearance == "clear-dark":
        return lambda lightness, chroma, hue: appicons.oklch(.3 + .55 * lightness, 0, 0)
    if appearance.startswith("tinted"):
        k = min(1, accent[1] / appicons.FULL_TINT_CHROMA)
        light = appearance == "tinted"
        return lambda lightness, chroma, hue: appicons.oklch(
            .62 + .3 * lightness if light else .5 + .45 * lightness,
            (min(chroma, .1) * .2 if light else min(chroma, .17) * .8) * k, accent[0])
    return None


def suffix_ids(text, suffix):
    ids = set(re.findall(r'\bid="([^"]+)"', text))
    rename = lambda m: m[0].replace(m[1], m[1] + suffix) if m[1] in ids else m[0]
    for pattern in (r'\bid="([^"]+)"', r"url\(#([^)]+)\)", r'href="#([^"]+)"'):
        text = re.sub(pattern, rename, text)
    return text


def nested(text, x, y, width, height):
    """The source SVG as an <svg> element of the tile, with its own viewBox."""
    root = ROOT.search(text)
    attrs = root[1]
    view_box = re.search(r'viewBox="([^"]+)"', attrs)
    box = view_box[1] if view_box else "0 0 {} {}".format(*(re.search(rf'\b{n}="([\d.]+)', attrs)[1] for n in ("width", "height")))
    attrs = re.sub(r'\s(?:width|height|viewBox|x|y)="[^"]*"', "", attrs)
    return f'<svg{attrs} x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" viewBox="{box}">{text[root.end():]}'


def icon(text, appearance, accent):
    image = resvg_py.svg_to_bytes(svg_string=text, width=128)
    image = Image.open(io.BytesIO(image)).convert("RGBA")
    colors = list(pixels(image))
    left, top, right, bottom = image.getchannel("A").point(lambda a: 255 if a > 25 else 0).getbbox() or (0, 0, 0, 0)
    if not colors or right == left:
        raise ValueError("nothing to draw")
    lobe, bright = plate_lobe(colors)
    c = appicons.colors(appearance, lobe.hue if lobe else 0, lobe.chroma if lobe else 0, accent)
    if appearance == "light":
        c["plate"] = logo_plate(lobe, bright)
    k = LOGO_SIDE / max(right - left, bottom - top)
    x, y = 512 - (left + right) / 2 * k, 512 - (top + bottom) / 2 * k
    place = lambda t: nested(t, x, y, image.width * k, image.height * k)
    convert = converter(appearance, accent)
    logo = recolor(text, convert) if convert else text
    cast = recolor(suffix_ids(text, "-cast"), lambda *_: "#000000")
    glass = appearance.startswith(("clear", "tinted"))
    content = f'<g opacity="{.2 if glass else .35}" transform="translate(0 18)">{place(cast)}</g>{place(logo)}'
    svg = appicons.tile(appearance, c, content)
    if build.skia_unsafe(svg):
        raise ValueError("<ellipse> that Skia draws wrong")
    return svg


def main():
    ap = argparse.ArgumentParser(description="Plate icons for the apps in a directory of SVG icons")
    ap.add_argument("icons", help="directory of SVG app icons, such as /usr/share/icons/hicolor/scalable/apps")
    ap.add_argument("--appearance", choices=APPEARANCES, default="light")
    ap.add_argument("--tint", help="#rrggbb accent, for the tinted appearances")
    ap.add_argument("--out", required=True, help="theme directory to write")
    a = ap.parse_args()
    if a.appearance.startswith("tinted") != bool(a.tint and re.fullmatch(r"#[0-9a-fA-F]{6}", a.tint)):
        sys.exit("tinted appearances need --tint #rrggbb; the others do not take one")
    accent = appicons.accent(a.tint) if a.tint else None
    drawn = set(build.APPS) | {os.path.splitext(f)[0] for f in os.listdir(build.APP_ART)}
    wanted = {}
    for f in sorted(os.listdir(a.icons)):
        name, ext = os.path.splitext(f)
        if ext != ".svg" or name in drawn:
            continue
        try:
            wanted[f"scalable/apps/{f}"] = icon(open(os.path.join(a.icons, f), encoding="utf-8").read(), a.appearance, accent)
        except (ValueError, TypeError) as error:
            print(f"{f}: {error}", file=sys.stderr)
    out = os.path.expanduser(a.out)
    parent = "Malaysia-Dark" if a.appearance.endswith("dark") else "Malaysia"
    build.sync(out, wanted, False, build.theme_index(os.path.basename(out.rstrip("/")), f"{parent} with app icons from {a.icons}",
                                                     parent, build.APP_DIRS))
    print(f"{len(wanted)} app icons written to {out}")


if __name__ == "__main__":
    main()
