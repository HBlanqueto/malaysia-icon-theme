"""App icon tile: the squircle of the Settings icon, a plate colored from a hue and a light rim.

light: a plate in the app's hue and a white figure.
dark:  a graphite plate and a figure in the app's color.
"""
import math

BODY = ("M100 724 L100 300 C100 185 170 100 300 100 L724 100 C854 100 924 185 924 300 "
        "L924 724 C924 839 854 924 724 924 L300 924 C170 924 100 839 100 724 Z")
NEUTRAL_CHROMA = .03


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


def vertical(id_, top, bottom, y1=0, y2=1, extra=""):
    return (f'<linearGradient id="{id_}" x1="0" y1="{y1}" x2="0" y2="{y2}"{extra}>'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>')


def colors(hue, chroma, dark):
    """(plate top, plate bottom, figure top, figure bottom, rim) of one appearance."""
    neutral = chroma < NEUTRAL_CHROMA
    rim = "#ffffff" if neutral else oklch(.97, .09, hue)
    if not dark:
        plate = ((oklch(.5, .012, 260), oklch(.34, .012, 260)) if neutral
                 else (oklch(.66, chroma, hue), oklch(.44, chroma * 1.05, hue + 8)))
        return *plate, "#ffffff", "#e6e9ef", rim
    figure = ("#eceef2", "#a9acb4") if neutral else (oklch(.82, chroma * .85, hue), oklch(.68, chroma, hue))
    return oklch(.29, 0, 0), oklch(.19, 0, 0), *figure, rim


def app_icon(figure, hue, chroma, dark):
    """`figure` is a stroke on the 16 px grid; hue and chroma are OKLCH."""
    plate_top, plate_bottom, figure_top, figure_bottom, rim = colors(hue, chroma, dark)
    stops = "".join(f'<stop offset="{at}" stop-color="{rim}" stop-opacity="{(.4 if dark else .45) * k:.3g}"/>'
                    for at, k in ((0, 1), (.3, .25), (.5, 0), (.75, .12), (1, .7)))
    stroke = f'fill="none" stroke-linecap="round" stroke-linejoin="round" d="{figure}"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs>'
            + vertical("plate", plate_top, plate_bottom)
            + vertical("figure", figure_top, figure_bottom, 2, 14, ' gradientUnits="userSpaceOnUse"')
            + f'<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'
            f'<clipPath id="clip"><path d="{BODY}"/></clipPath></defs>'
            f'<path d="{BODY}" fill="#000" fill-opacity=".1" transform="translate(0 14)"/>'
            f'<path d="{BODY}" fill="#000" fill-opacity=".12" transform="translate(0 6)"/>'
            f'<path d="{BODY}" fill="url(#plate)"/>'
            f'<path d="{BODY}" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="3"/>'
            f'<g clip-path="url(#clip)"><path d="{BODY}" fill="none" stroke="url(#rim)" stroke-width="24"/></g>'
            f'<g transform="translate(232 232) scale(35)" stroke-width="1.5">'
            f'<path stroke="#000" stroke-opacity=".25" transform="translate(0 .5)" {stroke}/>'
            f'<path stroke="url(#figure)" {stroke}/></g></svg>\n')
