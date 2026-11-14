"""The plate behind an app's own icon: the squircle of the Settings icon and a light rim.

Six appearances, measured on the macOS icon grid:
  light        a plate in the hue of the app's icon
  dark         a near black plate
  clear        a translucent white plate; clear-dark a translucent black one
  tinted       a plate in the accent; tinted-dark the translucent black one
The values are barrierkit's ICON_PLATE tokens.
"""
import math

BODY = ("M100 724 L100 300 C100 185 170 100 300 100 L724 100 C854 100 924 185 924 300 "
        "L924 724 C924 839 854 924 724 924 L300 924 C170 924 100 839 100 724 Z")
NEUTRAL_CHROMA = .03
FULL_TINT_CHROMA = .12  # an accent with less chroma gives a proportionally grayer icon; a gray gives a monochrome one
GLASS = {"clear": ("#ffffff", .2), "clear-dark": ("#000000", .66), "tinted-dark": ("#000000", .66)}
CORNER = (300, 300)  # the circle each corner of BODY turns on
EDGE_WIDTH = 16
LIGHT_REACH, LIGHT_SHARPNESS = 92, 3
LIGHT_SIDE = .6  # degrees of reach per grid unit down the side
OUTLINE_ENDS, OUTLINE_FROM, OUTLINE_TO = .28, 12, 84
WEDGE = 2


def srgb(linear):
    v = min(1, max(0, linear))
    return 12.92 * v if v <= .0031308 else 1.055 * v ** (1 / 2.4) - .055


def oklch(lightness, chroma, hue):
    """sRGB hex of an OKLCH color; the chroma shrinks until the color fits the gamut."""
    while True:
        a, b = chroma * math.cos(math.radians(hue)), chroma * math.sin(math.radians(hue))
        l, m, s = ((lightness + ka * a + kb * b) ** 3
                   for ka, kb in ((.3963377774, .2158037573), (-.1055613458, -.0638541728), (-.0894841775, -1.2914855480)))
        rgb = (4.0767416621 * l - 3.3077115913 * m + .2309699292 * s,
               -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s,
               -.0041960863 * l - .7034186147 * m + 1.7076147010 * s)
        if chroma <= 0 or all(-.002 < v < 1.002 for v in rgb):
            return "#" + "".join(f"{round(srgb(v) * 255):02x}" for v in rgb)
        chroma = max(0, chroma - .004)


def rgb_to_oklch(r, g, b):
    """(lightness, chroma, hue) of an 8-bit sRGB color."""
    lin = [((v / 255 + .055) / 1.055) ** 2.4 if v / 255 > .04045 else v / 255 / 12.92 for v in (r, g, b)]
    l, m, s = (math.cbrt(a * lin[0] + b * lin[1] + c * lin[2])
               for a, b, c in ((.4122214708, .5363325363, .0514459929), (.2119034982, .6806995451, .1073969566),
                               (.0883024619, .2817188376, .6299787005)))
    a = 1.9779984951 * l - 2.4285922050 * m + .4505937099 * s
    b = .0259040371 * l + .7827717662 * m - .8086757660 * s
    return .2104542553 * l + .7936177850 * m - .0040720468 * s, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def to_oklch(hex_):
    return rgb_to_oklch(*(int(hex_[i:i + 2], 16) for i in (1, 3, 5)))


def accent(hex_):
    """(hue, chroma) of a #rrggbb accent."""
    _, chroma, hue = to_oklch(hex_)
    return hue, chroma


def vertical(id_, top, bottom, opacity=(1, 1)):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}" stop-opacity="{opacity[0]}"/>'
            f'<stop offset="1" stop-color="{bottom}" stop-opacity="{opacity[1]}"/></linearGradient>')


def lifted(hex_, lift):
    """The Dock's toned rim: the color scaled per channel to `lift` more luma, with its own chroma."""
    rgb = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    luma = max(.001, .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2])
    scaled = "#" + "".join(f"{round(min(1, v * (luma + lift) / luma) * 255):02x}" for v in rgb)
    _, chroma, hue = to_oklch(hex_)
    return oklch(to_oklch(scaled)[0], chroma, hue)


def colors(appearance, hue, chroma, tint):
    """The plate gradient and opacity, the light along its top and bottom as ((color, opacity), ...), and the outline."""
    neutral = chroma < NEUTRAL_CHROMA
    white = lambda top, bottom: (("#ffffff", top), ("#ffffff", bottom))
    if appearance in GLASS:
        color, opacity = GLASS[appearance]
        outline = (oklch(.3, 0, 0), .9) if appearance == "clear" else ("#000000", .95)
        return dict(plate=(color, color), opacity=(opacity, opacity),
                    light=white(.6, .6) if appearance == "clear" else white(.2, .2), outline=outline)
    if appearance == "tinted":
        hue, accent = tint[0], min(1, tint[1] / FULL_TINT_CHROMA)
        top, bottom = oklch(.55, .15 * accent, hue), oklch(.48, .14 * accent, hue - 7)
        return dict(plate=(top, bottom), opacity=(1, 1), light=((lifted(top, .22), 1), (lifted(bottom, .22), 1)),
                    outline=(oklch(.275, .15 * accent, hue), 1))
    if appearance == "light":
        plate = ((oklch(.5, .012, 260), oklch(.34, .012, 260)) if neutral
                 else (oklch(.66, chroma, hue), oklch(.44, chroma * 1.05, hue + 8)))
        return dict(plate=plate, opacity=(1, 1), light=white(.45, .315), outline=None)
    return dict(plate=(oklch(.239, 0, 0), oklch(.173, 0, 0)), opacity=(1, 1), light=white(.3, .165), outline=None)


def corner_angles():
    """(x, angle of the edge from vertical) along BODY's top left corner."""
    p0, p1, p2, p3 = (100, 300), (100, 185), (170, 100), (300, 100)
    out = []
    for i in range(21):
        t = i / 20
        bezier = lambda a, b, c, d: (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
        slope = lambda a, b, c, d: 3 * (1 - t) ** 2 * (b - a) + 6 * (1 - t) * t * (c - b) + 3 * t ** 2 * (d - c)
        dx, dy = slope(p0[0], p1[0], p2[0], p3[0]), slope(p0[1], p1[1], p2[1], p3[1])
        out.append((bezier(p0[0], p1[0], p2[0], p3[0]), math.degrees(math.acos(abs(dx) / math.hypot(dx, dy)))))
    return out


def light_strength(angle):
    return math.exp(-(angle / LIGHT_REACH) ** LIGHT_SHARPNESS)


def outline_strength(angle):
    grow = (min(angle, 90) - OUTLINE_FROM) / (OUTLINE_TO - OUTLINE_FROM)
    return OUTLINE_ENDS + (1 - OUTLINE_ENDS) * min(1, max(0, grow))


def edge_mask(id_, strength):
    """Each point of the edge at strength(angle): the angle from vertical round each corner, and past 90 down the sides."""
    cx, cy = CORNER
    wedges = []
    for start in range(0, 90, WEDGE):
        a0, a1 = math.radians(start), math.radians(start + WEDGE)
        points = ((0, 0), (-500 * math.sin(a0), -500 * math.cos(a0)), (-500 * math.sin(a1), -500 * math.cos(a1)))
        for sx, sy, ox, oy in ((1, 1, cx, cy), (-1, 1, 1024 - cx, cy), (1, -1, cx, 1024 - cy), (-1, -1, 1024 - cx, 1024 - cy)):
            pts = " ".join(f"{ox + sx * x:.1f},{oy + sy * y:.1f}" for x, y in points)
            wedges.append(f'<polygon points="{pts}" fill-opacity="{strength(start + WEDGE / 2):.3f}"/>')
    span = 1024 - 2 * cy
    side = [(d, strength(90 + d * LIGHT_SIDE)) for d in range(0, span // 2, 10)]
    stops = "".join(f'<stop offset="{d / span:.4f}" stop-color="#fff" stop-opacity="{v:.3f}"/>' for d, v in side)
    stops += "".join(f'<stop offset="{1 - d / span:.4f}" stop-color="#fff" stop-opacity="{v:.3f}"/>' for d, v in reversed(side))
    # crispEdges: the zones meet without the seam antialiasing leaves between shapes
    return (f'<linearGradient id="{id_}-side" gradientUnits="userSpaceOnUse" x1="0" y1="{cy}" x2="0" y2="{1024 - cy}">{stops}</linearGradient>'
            f'<mask id="{id_}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1424" height="1424">'
            f'<g fill="#fff" shape-rendering="crispEdges">'
            f'<rect x="{cx}" y="-200" width="{1024 - 2 * cx}" height="1424" fill-opacity="{strength(0):.3f}"/>{"".join(wedges)}'
            f'<rect x="-200" y="{cy}" width="{cx + 200}" height="{span}" fill="url(#{id_}-side)"/>'
            f'<rect x="{1024 - cx}" y="{cy}" width="{cx + 200}" height="{span}" fill="url(#{id_}-side)"/></g></mask>')


def edge(light, outline=None):
    """The plate's light along its top and bottom edges, which turns each corner and ends in a point down the side,
    and the closed outline of clear and tinted plates, with the light just inside it. Returns its defs and its shapes."""
    (top, top_opacity), (bottom, bottom_opacity) = light
    defs = (vertical("light", top, bottom, (top_opacity, bottom_opacity)) + edge_mask("light-mask", light_strength)
            + f'<clipPath id="clip"><path d="{BODY}"/></clipPath>')
    depth = (4 if outline else 2) * EDGE_WIDTH
    shapes = f'<g mask="url(#light-mask)"><path d="{BODY}" fill="none" stroke="url(#light)" stroke-width="{depth}"/></g>'
    if outline:
        color, opacity = outline
        defs += edge_mask("outline-mask", outline_strength)
        shapes += (f'<g mask="url(#outline-mask)"><path d="{BODY}" fill="none" stroke="{color}" stroke-opacity="{opacity}" '
                   f'stroke-width="{2 * EDGE_WIDTH}"/></g>')
    return defs, f'<g clip-path="url(#clip)">{shapes}</g>'


def tile(appearance, c, content):
    """The squircle with its plate and edge; `c` comes from colors() and `content` is drawn on top."""
    shadow = .5 if appearance in GLASS else 1
    edge_defs, edge_shapes = edge(c["light"], c["outline"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs>'
            + vertical("plate", *c["plate"], c["opacity"]) + edge_defs + '</defs>'
            f'<path d="{BODY}" fill="#000" fill-opacity="{.1 * shadow:.3g}" transform="translate(0 14)"/>'
            f'<path d="{BODY}" fill="#000" fill-opacity="{.12 * shadow:.3g}" transform="translate(0 6)"/>'
            f'<path d="{BODY}" fill="url(#plate)"/>'
            f'{edge_shapes}{content}</svg>\n')
