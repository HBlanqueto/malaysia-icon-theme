#!/usr/bin/env python3
"""Exporta src/malaysia-symbolic/<contexto>/<nombre>.svg a Malaysia/symbolic/<contexto>/<nombre>.svg.

GTK pinta los íconos simbólicos forzando `fill` en cada rect, circle y path, y no toca
`stroke`. Por eso un trazo sin convertir se vería como una figura rellena. Este script
convierte los trazos en contornos rellenos con Skia (skia-pathops, vía picosvg) y deja un solo color (#2e3436),
como el resto del tema.

Uso: python3 tools/symbols/export.py [--check]
     --check  no escribe nada; termina con error si alguna exportación está desactualizada.

Requiere picosvg (pip install -r tools/requirements.txt).
"""
import os, re, sys
import pathops
from picosvg.svg import SVG
from picosvg.svg_pathops import skia_path, svg_commands
from picosvg.svg_transform import Affine2D
from picosvg.svg_types import SVGPath

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "src", "malaysia-symbolic")
OUT = os.path.join(ROOT, "Malaysia", "symbolic")
INK = "#2e3436"
# El trazador de Skia pierde precisión con coordenadas pequeñas (rejilla de 16): los arcos
# interiores salen con un solo segmento por cuadrante. Se amplía la figura, se traza y se reduce.
SCALE = 64
CAPS = {"butt": pathops.LineCap.BUTT_CAP, "round": pathops.LineCap.ROUND_CAP, "square": pathops.LineCap.SQUARE_CAP}
JOINS = {"miter": pathops.LineJoin.MITER_JOIN, "round": pathops.LineJoin.ROUND_JOIN, "bevel": pathops.LineJoin.BEVEL_JOIN}


def outline(shape, stroke):
    """Contorno relleno (Skia) de una figura, ya ampliado por SCALE."""
    path = shape.as_path().apply_transform(Affine2D.identity().scale(SCALE))
    sk = skia_path(path.as_cmd_seq(), fill_rule="nonzero" if stroke else shape.fill_rule)
    if stroke:
        sk.stroke(shape.stroke_width * SCALE, CAPS[shape.stroke_linecap], JOINS[shape.stroke_linejoin],
                  shape.stroke_miterlimit)
    sk.convertConicsToQuads(0.25)
    return sk


def convert(path):
    svg = SVG.parse(path)
    vb = svg.view_box()
    layers = {}  # opacidad → contorno unido
    for shape in svg.shapes():
        pieces = []
        if shape.fill not in ("none", "") and shape.fill_opacity > 0:
            pieces.append((outline(shape, False), shape.opacity * shape.fill_opacity))
        if shape.stroke not in ("none", "") and shape.stroke_width > 0 and shape.stroke_opacity > 0:
            pieces.append((outline(shape, True), shape.opacity * shape.stroke_opacity))
        for sk, alpha in pieces:
            alpha = round(alpha, 3)
            layers[alpha] = pathops.op(layers[alpha], sk, pathops.PathOp.UNION, fix_winding=True) if alpha in layers else sk
    body = []
    for alpha in sorted(layers, reverse=True):
        sk = layers[alpha]
        sk.simplify(fix_winding=True)
        d = SVGPath.from_commands(svg_commands(sk)).apply_transform(Affine2D.identity().scale(1 / SCALE)).round_floats(3).d
        body.append(f'<path fill="{INK}"' + (f' opacity="{alpha:g}"' if alpha < 1 else "") + f' d="{d}"/>')
    w, h = f"{vb.w:g}", f"{vb.h:g}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb.x:g} {vb.y:g} {w} {h}">'
            + "".join(body) + "</svg>\n")


def main(check):
    stale, written = [], 0
    for ctx in sorted(os.listdir(SRC)):
        for f in sorted(os.listdir(os.path.join(SRC, ctx))):
            if not f.endswith(".svg"):
                continue
            svg = convert(os.path.join(SRC, ctx, f))
            dest = os.path.join(OUT, ctx, f)
            # un nombre vive en un solo contexto: borrar la copia de Adwaita si estaba en otro
            others = [os.path.join(OUT, c, f) for c in os.listdir(OUT) if c != ctx and os.path.exists(os.path.join(OUT, c, f))]
            current = open(dest, encoding="utf-8").read() if os.path.exists(dest) else None
            if current != svg or others:
                stale.append(f"{ctx}/{f}")
                if not check:
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    open(dest, "w", encoding="utf-8").write(svg)
                    for o in others:
                        os.remove(o)
                    written += 1
    if check:
        if stale:
            sys.exit("desactualizados:\n  " + "\n  ".join(stale))
        print("todo al día")
    else:
        print(f"{written} archivos escritos en Malaysia/symbolic")


if __name__ == "__main__":
    main("--check" in sys.argv[1:])
