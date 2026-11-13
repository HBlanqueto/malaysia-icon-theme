"""App icon tile: the squircle of the Settings icon, a plate colored from a hue and a light rim.

Six appearances, measured on the macOS icon grid:
  light        a plate in the app's hue and a white figure
  dark         a graphite plate and a figure in the app's color
  clear        a translucent plate and a white-gray figure; clear-dark is dimmer
  tinted       a plate in the accent and a near-white figure; tinted-dark has a dark plate and an accent figure
"""
import math

BODY = ("M100 724 L100 300 C100 185 170 100 300 100 L724 100 C854 100 924 185 924 300 "
        "L924 724 C924 839 854 924 724 924 L300 924 C170 924 100 839 100 724 Z")
NEUTRAL_CHROMA = .03
FULL_TINT_CHROMA = .12  # an accent with less chroma gives a proportionally grayer icon; a gray gives a monochrome one
CLEAR = {"clear": ((.26, .17), ("#ffffff", "#cfd1d6")), "clear-dark": ((.17, .08), ("#f2f2f4", "#b6b8bd"))}


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


def vertical(id_, top, bottom, opacity=(1, 1), y1=0, y2=1, extra=""):
    return (f'<linearGradient id="{id_}" x1="0" y1="{y1}" x2="0" y2="{y2}"{extra}>'
            f'<stop offset="0" stop-color="{top}" stop-opacity="{opacity[0]}"/>'
            f'<stop offset="1" stop-color="{bottom}" stop-opacity="{opacity[1]}"/></linearGradient>')


def colors(appearance, hue, chroma, tint):
    """plate and figure gradients, the plate opacity, and the rim color and opacity."""
    neutral = chroma < NEUTRAL_CHROMA
    if appearance in CLEAR:
        opacity, figure = CLEAR[appearance]
        return dict(plate=("#ffffff", "#ffffff"), opacity=opacity, figure=figure, rim="#ffffff", rim_opacity=.5)
    if appearance.startswith("tinted"):
        hue, accent = tint[0], min(1, tint[1] / FULL_TINT_CHROMA)
        plate, figure = (((.52, .096), (.45, .085)), ((.97, .02), (.86, .04))) if appearance == "tinted" \
            else (((.3, .027), (.22, .014)), ((.78, .15), (.68, .16)))
        return dict(plate=(oklch(plate[0][0], plate[0][1] * accent, hue), oklch(plate[1][0], plate[1][1] * accent, hue - 7)),
                    opacity=(1, 1), figure=tuple(oklch(l, c * accent, hue) for l, c in figure),
                    rim=oklch(.97, .09 * accent, hue), rim_opacity=.4)
    rim = "#ffffff" if neutral else oklch(.97, .09, hue)
    if appearance == "light":
        plate = ((oklch(.5, .012, 260), oklch(.34, .012, 260)) if neutral
                 else (oklch(.66, chroma, hue), oklch(.44, chroma * 1.05, hue + 8)))
        return dict(plate=plate, opacity=(1, 1), figure=("#ffffff", "#e6e9ef"), rim=rim, rim_opacity=.45)
    figure = ("#eceef2", "#a9acb4") if neutral else (oklch(.82, chroma * .85, hue), oklch(.68, chroma, hue))
    return dict(plate=(oklch(.29, 0, 0), oklch(.19, 0, 0)), opacity=(1, 1), figure=figure, rim=rim, rim_opacity=.4)


def tile(appearance, c, content):
    """The squircle with its plate and rim; `c` comes from colors() and `content` is drawn on top."""
    shadow = .5 if appearance in CLEAR else 1
    stops = "".join(f'<stop offset="{at}" stop-color="{c["rim"]}" stop-opacity="{c["rim_opacity"] * k:.3g}"/>'
                    for at, k in ((0, 1), (.3, .25), (.5, 0), (.75, .12), (1, .7)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs>'
            + vertical("plate", *c["plate"], c["opacity"])
            + f'<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'
            f'<clipPath id="clip"><path d="{BODY}"/></clipPath></defs>'
            f'<path d="{BODY}" fill="#000" fill-opacity="{.1 * shadow:.3g}" transform="translate(0 14)"/>'
            f'<path d="{BODY}" fill="#000" fill-opacity="{.12 * shadow:.3g}" transform="translate(0 6)"/>'
            f'<path d="{BODY}" fill="url(#plate)"/>'
            f'<path d="{BODY}" fill="none" stroke="#000" stroke-opacity="{.12 * shadow:.3g}" stroke-width="3"/>'
            f'<g clip-path="url(#clip)"><path d="{BODY}" fill="none" stroke="url(#rim)" stroke-width="24"/></g>'
            f'{content}</svg>\n')


def app_icon(figure, hue, chroma, appearance, tint=None):
    """`figure` is a stroke on the 16 px grid; hue and chroma are OKLCH; `tint` is (hue, chroma) of the accent."""
    c = colors(appearance, hue, chroma, tint)
    stroke = f'fill="none" stroke-linecap="round" stroke-linejoin="round" d="{figure}"'
    return tile(appearance, c, '<defs>' + vertical("figure", *c["figure"], (1, 1), 2, 14, ' gradientUnits="userSpaceOnUse"')
                + '</defs><g transform="translate(232 232) scale(35)" stroke-width="1.5">'
                f'<path stroke="#000" stroke-opacity=".25" transform="translate(0 .5)" {stroke}/>'
                f'<path stroke="url(#figure)" {stroke}/></g>')
