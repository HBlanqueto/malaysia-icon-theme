#!/usr/bin/env python3
"""Write src/malaysia-symbolic/status/battery-percent-<1..100>-symbolic.svg.

The battery of battery-level-*, with the percentage knocked out of the body as on macOS 27.
The digits are the semibold digits of Inter 5.0.8 (SIL OFL 1.1, COPYING_OFL) at a 10 unit
font size, as (width, x0, y0, relative path) from the box of each glyph. Skia does the
subtraction, so the source is two filled paths and GTK needs no mask.

Usage: python3 tools/symbols/battery_percent.py [--check]
       --check  write nothing; exit with an error if a source is out of date.

Requires picosvg (pip install -r tools/requirements.txt).
"""
import os, sys
import pathops
from picosvg.svg_pathops import skia_path, svg_commands
from picosvg.svg_transform import Affine2D
from picosvg.svg_types import SVGPath

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "src", "malaysia-symbolic", "status")
INK = "#2e3436"
BODY_WIDTH = 13
BODY = "M2 3 L11 3 C12.1 3 13 3.9 13 5 L13 11 C13 12.1 12.1 13 11 13 L2 13 C0.9 13 0 12.1 0 11 L0 5 C0 3.9 0.9 3 2 3 Z"
NUB = "M14 6 C15.1 6 16 6.9 16 8 C16 9.1 15.1 10 14 10 Z"
LEVEL_MIN = 0.8
BODY_CENTER = 8
DIGIT_HEIGHT = 7.27
GAP = 1.0
SCALE = {1: 0.7, 2: 0.7, 3: 0.62}
DIGITS = {
    "0": (5.6, 2.79, 7.41, "q-.88 0-1.51-.44q-.62-.45-.96-1.29q-.33-.85-.33-2.04q0-1.19 .33-2.02q.34-.84 .97-1.28q.62-.44 1.5-.44q.87 0 1.5 .44q.63 .44 .96 1.28q.34 .84 .34 2.02q0 1.2-.34 2.04q-.33 .84-.96 1.29q-.63 .44-1.5 .44zm0-1.11q.68 0 1.08-.67q.39-.68 .39-1.99q0-.86-.18-1.45q-.18-.59-.51-.89q-.33-.3-.78-.3q-.68 0-1.07 .67q-.4 .67-.4 1.97q-.01 .87 .17 1.47q.18 .59 .51 .89q.33 .3 .79 .3z"),
    "1": (3.06, 3.06, 0, "v7.27h-1.32v-5.99h-.04l-1.7 1.09v-1.21l1.8-1.16z"),
    "2": (5.03, 0.1, 7.27, "v-.95l2.52-2.47q.37-.37 .61-.65q.24-.29 .36-.55q.12-.27 .12-.57q0-.35-.16-.59q-.15-.25-.43-.39q-.27-.13-.62-.13q-.36 0-.62 .15q-.27 .14-.42 .41q-.15 .27-.15 .65h-1.25q0-.7 .31-1.21q.32-.51 .87-.79q.56-.28 1.28-.28q.73 0 1.29 .27q.55 .28 .86 .75q.31 .48 .31 1.09q0 .41-.16 .8q-.16 .4-.55 .88q-.39 .48-1.1 1.16l-1.25 1.27v.05h3.17v1.1z"),
    "3": (5.36, 2.71, 7.37, "q-.77 0-1.36-.26q-.6-.26-.94-.73q-.35-.47-.37-1.09h1.34q.02 .3 .19 .52q.18 .22 .48 .34q.29 .12 .66 .12q.39 0 .69-.14q.3-.14 .47-.38q.17-.25 .17-.57q0-.33-.17-.58q-.18-.25-.51-.39q-.32-.14-.79-.14h-.64v-1.02h.64q.38 0 .67-.13q.29-.13 .45-.37q.16-.24 .16-.56q0-.31-.14-.54q-.14-.22-.39-.35q-.26-.13-.6-.13q-.33 0-.61 .12q-.29 .12-.46 .34q-.18 .22-.19 .53h-1.26q.01-.61 .35-1.07q.34-.47 .91-.73q.56-.26 1.27-.26q.73 0 1.27 .27q.53 .27 .83 .73q.29 .46 .29 1.01q.01 .62-.36 1.03q-.36 .42-.95 .55v.05q.77 .11 1.18 .57q.41 .46 .4 1.14q0 .61-.34 1.09q-.35 .49-.95 .76q-.61 .27-1.39 .27z"),
    "4": (5.66, -0.03, 5.92, "v-1.04l3.08-4.88h1.64v4.84h.93v1.08h-.93v1.35h-1.25v-1.35zm3.48-1.08v-3.35h-.06l-2.07 3.29v.06z"),
    "5": (5.12, 2.63, 7.37, "q-.71 0-1.27-.27q-.56-.26-.89-.73q-.33-.47-.35-1.08h1.28q.03 .45 .38 .73q.35 .29 .85 .29q.38 0 .69-.18q.3-.18 .47-.49q.18-.32 .17-.73q.01-.41-.17-.73q-.18-.32-.49-.5q-.31-.18-.71-.18q-.32-.01-.64 .12q-.32 .12-.5 .33l-1.19-.2l.38-3.75h4.22v1.1h-3.13l-.21 1.93h.04q.2-.24 .57-.4q.37-.15 .81-.15q.66 0 1.18 .31q.52 .31 .82 .85q.3 .54 .3 1.24q0 .72-.33 1.29q-.34 .56-.92 .88q-.59 .32-1.36 .32z"),
    "6": (5.4, 2.76, 7.37, "q-.52 0-1.02-.18q-.49-.18-.89-.59q-.4-.4-.63-1.08q-.24-.68-.23-1.68q0-.93 .19-1.66q.2-.73 .58-1.24q.37-.51 .9-.77q.52-.27 1.18-.27q.68 0 1.21 .27q.53 .27 .86 .74q.33 .46 .41 1.05h-1.3q-.1-.42-.41-.67q-.3-.25-.77-.25q-.76 0-1.17 .66q-.4 .65-.41 1.8h.05q.18-.31 .45-.53q.28-.23 .63-.35q.35-.12 .74-.12q.64 0 1.15 .3q.51 .31 .81 .84q.3 .54 .29 1.23q.01 .71-.32 1.28q-.33 .57-.92 .9q-.59 .33-1.38 .32zm0-1.06q.38 0 .69-.19q.3-.19 .48-.51q.18-.32 .18-.72q0-.39-.17-.7q-.18-.32-.48-.5q-.3-.19-.69-.19q-.28 0-.53 .11q-.25 .11-.44 .31q-.18 .19-.29 .44q-.1 .26-.1 .54q0 .38 .17 .7q.18 .32 .48 .52q.31 .19 .7 .19z"),
    "7": (4.95, 0.37, 7.27, "l3.09-6.12v-.05h-3.59v-1.1h4.95v1.13l-3.09 6.14z"),
    "8": (5.41, 2.68, 7.37, "q-.79 0-1.4-.26q-.61-.27-.96-.73q-.34-.47-.34-1.06q0-.45 .2-.84q.2-.38 .55-.64q.34-.26 .77-.33v-.05q-.56-.12-.91-.57q-.34-.45-.34-1.04q0-.56 .31-1q.32-.44 .87-.7q.55-.25 1.25-.25q.7 0 1.25 .25q.55 .26 .87 .7q.32 .44 .32 1q0 .59-.35 1.04q-.35 .45-.9 .57v.05q.42 .07 .77 .33q.34 .26 .54 .64q.21 .39 .21 .84q0 .59-.35 1.06q-.35 .46-.96 .73q-.61 .26-1.4 .26zm0-1.01q.41 0 .71-.14q.31-.14 .47-.4q.17-.26 .17-.59q0-.35-.18-.62q-.17-.26-.47-.42q-.31-.15-.7-.15q-.39 0-.69 .15q-.31 .16-.48 .42q-.18 .27-.17 .62q-.01 .33 .16 .59q.17 .25 .47 .39q.3 .15 .71 .15zm0-3.32q.34 0 .6-.13q.25-.14 .4-.38q.15-.24 .16-.56q-.01-.31-.15-.54q-.15-.24-.41-.37q-.26-.13-.6-.13q-.34 0-.6 .13q-.26 .13-.41 .37q-.14 .23-.14 .54q0 .32 .15 .56q.15 .24 .41 .38q.26 .13 .59 .13z"),
    "9": (5.4, 2.62, -0.1, "q.53 0 1.02 .18q.5 .18 .89 .59q.4 .4 .64 1.07q.23 .68 .23 1.67q0 .94-.2 1.68q-.2 .73-.57 1.24q-.37 .51-.9 .78q-.52 .26-1.18 .26q-.69 0-1.22-.27q-.53-.27-.86-.74q-.32-.47-.4-1.07h1.3q.1 .43 .4 .69q.31 .25 .78 .25q.76 0 1.16-.65q.41-.66 .41-1.83h-.05q-.17 .31-.45 .54q-.27 .22-.62 .34q-.35 .12-.75 .12q-.63 0-1.14-.3q-.51-.31-.81-.84q-.3-.53-.3-1.22q0-.71 .33-1.27q.33-.57 .92-.9q.59-.33 1.37-.32zm.01 1.07q-.39 0-.69 .18q-.31 .19-.49 .51q-.17 .31-.17 .71q0 .38 .17 .7q.18 .31 .48 .5q.3 .18 .68 .18q.29 0 .54-.11q.25-.11 .43-.3q.19-.2 .3-.45q.1-.26 .1-.54q0-.37-.18-.68q-.17-.32-.48-.51q-.3-.19-.69-.19z"),
}


def path(d, transform=Affine2D.identity()):
    return skia_path(SVGPath(d=d).apply_transform(transform).as_cmd_seq(), fill_rule="nonzero")


def digits(percent):
    text = str(percent)
    k = SCALE[len(text)]
    width = sum(DIGITS[c][0] for c in text) + GAP * (len(text) - 1)
    x = (BODY_WIDTH - width * k) / 2
    y = BODY_CENTER - DIGIT_HEIGHT * k / 2
    glyphs = []
    for c in text:
        w, x0, y0, rest = DIGITS[c]
        glyphs.append(path(f"M{x0} {y0}{rest}", Affine2D(k, 0, 0, k, x, y)))
        x += (w + GAP) * k
    return glyphs


def d(sk):
    sk.simplify(fix_winding=True)
    return SVGPath.from_commands(svg_commands(sk)).round_floats(3).d


def source(percent):
    knockout = pathops.Path()
    for glyph in digits(percent):
        knockout = pathops.op(knockout, glyph, pathops.PathOp.UNION, fix_winding=True)
    level = max(BODY_WIDTH * percent / 100, LEVEL_MIN)
    body = path(BODY)
    left = pathops.op(body, path(f"M0 0H{level:g}V16H0Z"), pathops.PathOp.INTERSECTION, fix_winding=True)
    right = pathops.op(body, path(f"M{level:g} 0H16V16H{level:g}Z"), pathops.PathOp.INTERSECTION, fix_winding=True)
    fill = pathops.op(left, knockout, pathops.PathOp.DIFFERENCE, fix_winding=True)
    track = pathops.op(right, knockout, pathops.PathOp.DIFFERENCE, fix_winding=True)
    track = pathops.op(track, path(NUB), pathops.PathOp.UNION, fix_winding=True)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
            f'<path d="{d(fill)}" fill="{INK}"/><path d="{d(track)}" fill="{INK}" opacity="0.5"/></svg>\n')


def main(check):
    stale = []
    for percent in range(1, 101):
        name = f"battery-percent-{percent}-symbolic.svg"
        dest = os.path.join(OUT, name)
        svg = source(percent)
        current = open(dest, encoding="utf-8").read() if os.path.exists(dest) else None
        if current != svg:
            stale.append(name)
            if not check:
                open(dest, "w", encoding="utf-8").write(svg)
    if check:
        if stale:
            sys.exit("out of date:\n  " + "\n  ".join(stale))
        print("up to date")
    else:
        print(f"{len(stale)} files written to src/malaysia-symbolic/status")


if __name__ == "__main__":
    main("--check" in sys.argv[1:])
