"""Device icons rendered like macOS hardware icons.

Apple's guidance for macOS icons asks for lifelike rendering: a front-facing, level view,
one consistent drop shadow, and objects that look made of physical materials with mass.
Edges come from light, never from an outline. The reference is the macOS 26.1 drive icon:
aluminum with rounded, cylindrically lit sides, a beveled top edge, a rounded bottom face
with its own volume, and marks pressed into the metal with a soft inner shadow.
"""
import math

# one drop shadow for every device, folder and document: a soft cast shadow plus a tight contact shadow
DROP = (
    '<filter id="drop" x="-25%" y="-25%" width="150%" height="160%">'
    '<feGaussianBlur in="SourceAlpha" stdDeviation="1.6"/><feOffset dy="1.8" result="far"/>'
    '<feFlood flood-color="#000000" flood-opacity=".26"/><feComposite in2="far" operator="in" result="cast"/>'
    '<feGaussianBlur in="SourceAlpha" stdDeviation=".35"/><feOffset dy=".45" result="near"/>'
    '<feFlood flood-color="#000000" flood-opacity=".3"/><feComposite in2="near" operator="in" result="contact"/>'
    '<feMerge><feMergeNode in="cast"/><feMergeNode in="contact"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
)
# a mark pressed into the surface: shadow inside its upper edge
INSET = (
    '<filter id="inset" x="-30%" y="-30%" width="160%" height="160%">'
    '<feComponentTransfer in="SourceAlpha"><feFuncA type="table" tableValues="1 0"/></feComponentTransfer>'
    '<feGaussianBlur stdDeviation=".55"/><feOffset dy=".7" result="edge"/>'
    '<feFlood flood-color="#000000" flood-opacity=".5"/><feComposite in2="edge" operator="in"/>'
    '<feComposite in2="SourceAlpha" operator="in" result="shade"/>'
    '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shade"/></feMerge></filter>'
)
DEFS = (
    DROP + INSET +
    '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation=".45"/></filter>'
    # aluminum
    '<linearGradient id="alu" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#dadbde"/><stop offset=".5" stop-color="#c6c8cb"/><stop offset="1" stop-color="#aeb0b4"/></linearGradient>'
    '<linearGradient id="alu-dark" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#c9cbcf"/><stop offset="1" stop-color="#999ba0"/></linearGradient>'
    '<linearGradient id="side" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#000000" stop-opacity=".28"/><stop offset=".008" stop-color="#ffffff" stop-opacity=".55"/>'
    '<stop offset=".022" stop-color="#ffffff" stop-opacity=".2"/><stop offset=".05" stop-color="#000000" stop-opacity=".14"/>'
    '<stop offset=".09" stop-color="#000000" stop-opacity=".04"/><stop offset=".16" stop-color="#ffffff" stop-opacity=".12"/>'
    '<stop offset=".35" stop-color="#ffffff" stop-opacity="0"/><stop offset=".84" stop-color="#000000" stop-opacity="0"/>'
    '<stop offset=".91" stop-color="#000000" stop-opacity=".06"/><stop offset=".95" stop-color="#000000" stop-opacity=".16"/>'
    '<stop offset=".978" stop-color="#ffffff" stop-opacity=".2"/><stop offset=".992" stop-color="#ffffff" stop-opacity=".5"/>'
    '<stop offset="1" stop-color="#000000" stop-opacity=".3"/></linearGradient>'
    '<linearGradient id="bevel" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".025" stop-color="#ffffff" stop-opacity=".25"/>'
    '<stop offset=".06" stop-color="#ffffff" stop-opacity="0"/><stop offset=".94" stop-color="#000000" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#000000" stop-opacity=".22"/></linearGradient>'
    '<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#a6a8ac"/><stop offset=".12" stop-color="#8b8d92"/><stop offset=".6" stop-color="#7c7e83"/>'
    '<stop offset="1" stop-color="#606267"/></linearGradient>'
    '<linearGradient id="lip-dark" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#45474d"/><stop offset=".2" stop-color="#26282c"/><stop offset="1" stop-color="#0c0d0f"/></linearGradient>'
    '<linearGradient id="blue-alu" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#6c9de3"/><stop offset=".5" stop-color="#3a6ec4"/><stop offset="1" stop-color="#22498f"/></linearGradient>'
    '<linearGradient id="green" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#7be08a"/><stop offset=".5" stop-color="#34b552"/><stop offset="1" stop-color="#1d8a35"/></linearGradient>'
    '<linearGradient id="pcb" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#3fa95c"/><stop offset=".5" stop-color="#23803f"/><stop offset="1" stop-color="#15582b"/></linearGradient>'
    # frosted plastic bin
    '<linearGradient id="bin" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ffffff" stop-opacity=".76"/><stop offset="1" stop-color="#e2e4e8" stop-opacity=".86"/></linearGradient>'
    '<linearGradient id="bin-dark" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#6b6e74" stop-opacity=".9"/><stop offset="1" stop-color="#36383d" stop-opacity=".95"/></linearGradient>'
    '<linearGradient id="bin-inside" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#c9ccd2"/><stop offset="1" stop-color="#f4f5f7"/></linearGradient>'
    '<linearGradient id="bin-inside-dark" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#26282c"/><stop offset="1" stop-color="#55585e"/></linearGradient>'
    '<linearGradient id="frost" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset=".08" stop-color="#ffffff" stop-opacity="0"/><stop offset=".2" stop-color="#ffffff" stop-opacity=".55"/>'
    '<stop offset=".32" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
    '<filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2"/></filter>'
    '<radialGradient id="globe" cx=".36" cy=".3" r=".8">'
    '<stop offset="0" stop-color="#8fdcff"/><stop offset=".5" stop-color="#1e8cf0"/><stop offset="1" stop-color="#0b3e9c"/></radialGradient>'
    '<linearGradient id="lip-white" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#e6e8eb"/><stop offset="1" stop-color="#bfc2c8"/></linearGradient>'
    # plastic, steel, glass
    '<linearGradient id="plastic" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#f3f4f6"/><stop offset="1" stop-color="#dfe1e5"/></linearGradient>'
    '<linearGradient id="steel" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#8e9096"/><stop offset=".18" stop-color="#e9eaed"/><stop offset=".45" stop-color="#b9bbc0"/>'
    '<stop offset=".7" stop-color="#f4f5f7"/><stop offset="1" stop-color="#8e9096"/></linearGradient>'
    '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#26282e"/><stop offset="1" stop-color="#08090b"/></linearGradient>'
    '<linearGradient id="reflect" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#ffffff" stop-opacity=".18"/><stop offset=".42" stop-color="#ffffff" stop-opacity=".06"/>'
    '<stop offset=".43" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
    '<linearGradient id="crystal" x1="0" y1="0" x2=".7" y2="1">'
    '<stop offset="0" stop-color="#4fdcff"/><stop offset=".55" stop-color="#1e9bf5"/><stop offset="1" stop-color="#1565e0"/></linearGradient>'
    '<linearGradient id="graphite" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#4a4c52"/><stop offset=".5" stop-color="#2c2e33"/><stop offset="1" stop-color="#18191c"/></linearGradient>'
    '<radialGradient id="platter" cx=".38" cy=".3" r=".8">'
    '<stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="#cfd2d8"/><stop offset=".75" stop-color="#9ea2aa"/>'
    '<stop offset="1" stop-color="#e2e4e8"/></radialGradient>'
    '<linearGradient id="label" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#3d8bff"/><stop offset="1" stop-color="#1048c8"/></linearGradient>'
    '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#f6df9c"/><stop offset=".5" stop-color="#d6ae55"/><stop offset="1" stop-color="#b48a33"/></linearGradient>'
    '<radialGradient id="cone" cx=".42" cy=".36" r=".72">'
    '<stop offset="0" stop-color="#55585f"/><stop offset=".55" stop-color="#25272c"/><stop offset="1" stop-color="#0c0d0f"/></radialGradient>'
    '<radialGradient id="lens" cx=".38" cy=".32" r=".75">'
    '<stop offset="0" stop-color="#5a7fd0"/><stop offset=".45" stop-color="#1a2a55"/><stop offset="1" stop-color="#030409"/></radialGradient>'
    '<radialGradient id="disc" cx=".5" cy=".5" r=".5">'
    '<stop offset=".18" stop-color="#fbfbfc"/><stop offset=".7" stop-color="#d9dbe0"/><stop offset="1" stop-color="#b5b8bf"/></radialGradient>'
    '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset=".18" stop-color="#ff7ad9" stop-opacity="0"/><stop offset=".36" stop-color="#ff7ad9" stop-opacity=".42"/>'
    '<stop offset=".5" stop-color="#5fd3ff" stop-opacity=".42"/><stop offset=".63" stop-color="#9dff7a" stop-opacity=".34"/>'
    '<stop offset=".8" stop-color="#ffe066" stop-opacity="0"/></linearGradient>'
    '<linearGradient id="sheen2" x1="1" y1="0" x2="0" y2="1">'
    '<stop offset=".3" stop-color="#ffffff" stop-opacity="0"/><stop offset=".48" stop-color="#ffffff" stop-opacity=".55"/>'
    '<stop offset=".56" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
    '<pattern id="mesh" width="1.3" height="1.3" patternUnits="userSpaceOnUse">'
    '<circle cx=".65" cy=".65" r=".33" fill="#000000" fill-opacity=".55"/></pattern>'
    '<pattern id="mesh-light" width="1.1" height="1.1" patternUnits="userSpaceOnUse">'
    '<circle cx=".55" cy=".55" r=".28" fill="#ffffff" fill-opacity=".5"/></pattern>'
)


def rr(x, y, w, h, r):
    return (f'M{x + r:g} {y:g}h{w - 2 * r:g}a{r:g} {r:g} 0 0 1 {r:g} {r:g}v{h - 2 * r:g}a{r:g} {r:g} 0 0 1-{r:g} {r:g}'
            f'h-{w - 2 * r:g}a{r:g} {r:g} 0 0 1-{r:g}-{r:g}v-{h - 2 * r:g}a{r:g} {r:g} 0 0 1 {r:g}-{r:g}z')


def solid(d, fill="alu"):
    """A volume of material: base color, cylindrical side light and a beveled top edge."""
    return (f'<path d="{d}" fill="url(#{fill})"/><path d="{d}" fill="url(#side)"/>'
            f'<path d="{d}" fill="url(#bevel)"/>')


def body(x, y, w, h, r, fill="alu"):
    return solid(rr(x, y, w, h, r), fill)


def lip(x, y, w, h, fill="lip"):
    """The rounded bottom face, seen from just above: its own volume and a lit front edge."""
    d = rr(x, y, w, h, h / 2)
    return (f'<path d="{d}" fill="url(#{fill})"/><path d="{d}" fill="url(#side)"/>'
            f'<path d="M{x + h / 2} {y + .35}h{w - h}" stroke="#ffffff" stroke-opacity=".5" stroke-width=".5" stroke-linecap="round"/>')


def deboss(d, fill="#b8babe"):
    """A mark pressed into the surface, with a light lower rim and a soft inner shadow."""
    return (f'<path d="{d}" fill="#ffffff" fill-opacity=".55" transform="translate(0 .4)"/>'
            f'<path d="{d}" fill="{fill}" filter="url(#inset)"/>')


def glass(x, y, w, h, r):
    d = rr(x, y, w, h, r)
    return f'<path d="{d}" fill="url(#glass)"/>'


def screen(x, y, w, h, r):
    d = rr(x, y, w, h, r)
    return f'<path d="{d}" fill="url(#crystal)"/>'


def reflection(x, y, w, h, r):
    return f'<path d="{rr(x, y, w, h, r)}" fill="url(#reflect)"/>'


def ring(cx, cy, r_out, r_in):
    return (f'M{cx} {cy - r_out}a{r_out} {r_out} 0 1 1 0 {2 * r_out}a{r_out} {r_out} 0 1 1 0-{2 * r_out}z'
            f'M{cx} {cy - r_in}a{r_in} {r_in} 0 1 0 0 {2 * r_in}a{r_in} {r_in} 0 1 0 0-{2 * r_in}z')


def emblem(cx, cy, r, fig, fill="url(#label)"):
    """A round seal with a symbol stroked in white; `fig` is a path on the 16 px grid."""
    k = r * .8 / 9
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff"/><circle cx="{cx}" cy="{cy}" r="{r - 1.2:g}" fill="{fill}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 1.2:g}" fill="url(#bevel)"/>'
            f'<g transform="translate({cx - 8 * k:g} {cy - 8 * k:g}) scale({k:g})"><path fill="none" stroke="#ffffff" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="{fig}"/></g>')


def badge(fig, fill="url(#label)"):
    return emblem(51, 13, 9, fig, fill)


def circle(cx, cy, r):
    return f'M{cx} {cy - r}a{r} {r} 0 1 1 0 {2 * r}a{r} {r} 0 1 1 0-{2 * r}z'


def sector(cx, cy, r_in, r_out, a0, a1, color):
    pt = lambda r, a: f"{cx + r * math.cos(math.radians(a)):.2f} {cy + r * math.sin(math.radians(a)):.2f}"
    big = int(a1 - a0 > 180)
    return (f'<path d="M{pt(r_out, a0)}A{r_out} {r_out} 0 {big} 1 {pt(r_out, a1)}L{pt(r_in, a1)}'
            f'A{r_in} {r_in} 0 {big} 0 {pt(r_in, a0)}z" fill="{color}" fill-opacity=".55"/>')


def drive(x, y, w, h, fill="alu", base="lip"):
    """A body whose bottom face shows as a thin, darker band the full width of the body."""
    band = round(max(7, h * .14), 1)
    return body(x, y, w, h, round(max(3.6, w * .12), 1), fill) + lip(x, y + h - band, w, band, base)


def led(cx, cy, color="#30d158"):
    return (f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{color}" fill-opacity=".3" filter="url(#soft)"/>'
            f'<circle cx="{cx}" cy="{cy}" r=".9" fill="{color}"/>')


def screw(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="1.3" fill="url(#steel)" filter="url(#inset)"/>'
            f'<path d="M{cx - .7} {cy}h1.4" stroke="#5c5f66" stroke-width=".45"/>')


def harddisk(partitions=()):
    """An open 3.5-inch drive seen from above: platter, spindle, actuator arm and label."""
    platter = ring(32, 25, 19, 4.6)
    arm = "M46.6 47.6 35.4 31.6a1.3 1.3 0 0 1 2-1.5l12.8 15.2z"
    label = rr(13.5, 48, 22, 8.6, 1.2)
    return (body(9, 3, 46, 57, 4) + deboss(rr(11.4, 5.4, 41.2, 52.2, 2.6), "#c3c5c9")
            + f'<path fill-rule="evenodd" d="{ring(32, 25, 19.8, 19)}" fill="#000000" fill-opacity=".25" filter="url(#soft)"/>'
            + f'<path fill-rule="evenodd" d="{platter}" fill="url(#platter)"/>'
            + f'<path fill-rule="evenodd" d="{platter}" fill="url(#sheen2)"/>'
            + "".join(sector(32, 25, 6, 18.4, a0, a1, color) for a0, a1, color in partitions)
            + '<circle cx="32" cy="25" r="4.6" fill="url(#steel)"/><circle cx="32" cy="25" r="1.6" fill="#3a3c41"/>'
            + "".join(f'<circle cx="{32 + 3.1 * c:.2f}" cy="{25 + 3.1 * s:.2f}" r=".45" fill="#5c5f66"/>'
                      for c, s in ((1, 0), (-.5, .866), (-.5, -.866)))
            + f'<path d="{arm}" fill="#000000" fill-opacity=".3" filter="url(#soft)" transform="translate(.6 .8)"/>'
            + solid(arm, "steel") + '<rect x="34.4" y="29.4" width="2.6" height="1.6" rx=".5" fill="#2c2e33" transform="rotate(50 35.7 30.2)"/>'
            + '<circle cx="47.4" cy="48.4" r="4.4" fill="url(#graphite)"/><circle cx="47.4" cy="48.4" r="1.6" fill="url(#steel)"/>'
            + f'<path d="{label}" fill="url(#plastic)"/>'
            + '<path d="M16 51h11M16 53.4h16" stroke="#a9acb3" stroke-width=".9" stroke-linecap="round"/>'
            + '<rect x="16" y="55.2" width="5" height=".7" fill="#1565e0"/>'
            + "".join(screw(x, y) for x, y in ((13.4, 7.4), (50.6, 7.4), (50.6, 55.6))))


def multidisk():
    return (f'<g transform="translate(9 -1) scale(.82)" opacity=".9">{harddisk()}</g>'
            f'<g transform="translate(1 9) scale(.82)">{harddisk()}</g>')


def removable_drive():
    cable = ('<path d="M48 41h4.5a4 4 0 0 1 4 4v5" fill="none" stroke="#6f7176" stroke-width="3.4" stroke-linecap="round"/>'
             '<path d="M48 41h4.5a4 4 0 0 1 4 4v5" fill="none" stroke="#eceef1" stroke-width="2.2" stroke-linecap="round"/>'
             '<path d="M48 40.6h4.5a4.4 4.4 0 0 1 4.4 4.4" fill="none" stroke="#ffffff" stroke-width=".6" stroke-linecap="round"/>'
             + body(53.6, 48.6, 5.8, 7, 1.4, "steel"))
    light = ('<rect x="16" y="43.2" width="26" height="1.2" rx=".6" fill="#5ac8fa"/>'
             '<rect x="15" y="42.2" width="28" height="3.2" rx="1.6" fill="#5ac8fa" fill-opacity=".35" filter="url(#soft)"/>')
    return cable + drive(8, 17, 42, 36, "graphite", "lip-dark") + deboss(ring(29, 29, 5.8, 2), "#1d1e21") + light


def optical_drive():
    d = ring(32, 25, 18, 2.4)
    disc = (f'<path fill-rule="evenodd" d="{d}" fill="url(#disc)"/><path fill-rule="evenodd" d="{d}" fill="url(#sheen)"/>'
            f'<path fill-rule="evenodd" d="{d}" fill="url(#sheen2)"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 25, 7, 2.4)}" fill="#ffffff" fill-opacity=".5"/>')
    eject = "M47.6 38.4l2.8-3.2 2.8 3.2zM47.6 40h5.6"
    return disc + body(4, 29, 56, 18, 5) + lip(4, 41.5, 56, 5.5) + deboss(rr(11, 36, 31, 2.6, 1.3), "#2c2e33") + deboss(eject)


def optical_disc():
    d = ring(32, 29, 24.5, 2.8)
    return (f'<path fill-rule="evenodd" d="{d}" fill="url(#disc)"/>'
            f'<path fill-rule="evenodd" d="{d}" fill="url(#sheen)"/>'
            f'<path fill-rule="evenodd" d="{d}" fill="url(#sheen2)"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 29, 9, 2.8)}" fill="#ffffff" fill-opacity=".6"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 29, 4.4, 2.8)}" fill="#c9ccd2" fill-opacity=".8"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 29, 24.5, 24)}" fill="#ffffff" fill-opacity=".8"/>')


def usb_stick():
    return (body(25.5, 3.5, 13, 13, 1.4, "steel") + '<rect x="28" y="6.6" width="8" height="3.4" rx="1" fill="#1f2125"/>'
            + '<rect x="28.8" y="7.4" width="2" height="1.6" fill="#d6ae55"/><rect x="33.2" y="7.4" width="2" height="1.6" fill="#d6ae55"/>'
            + drive(21, 14, 22, 44, "blue-alu", "lip-dark") + deboss(ring(32, 44, 2.8, 1.7), "#1d3f7c")
            + led(32, 22, "#ffffff"))


def sd_card():
    d = "M18 6h22l9 9v39a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V9a3 3 0 0 1 3-3z"
    contacts = "".join(f'<rect x="{19.2 + i * 3.6:.1f}" y="8.4" width="2.4" height="8.4" rx=".7" fill="url(#gold)"/>'
                       for i in range(6))
    label = rr(19, 26, 26, 25, 2.8)
    return (solid(d, "graphite") + contacts + deboss(rr(13.4, 29, 2.2, 9, .9), "#8e9096")
            + f'<path d="{label}" fill="url(#label)"/><path d="{label}" fill="url(#bevel)"/>'
            + '<path d="M19 30c8 0 17-1.6 26-4.2V28.8a2.8 2.8 0 0 0-2.8-2.8H21.8A2.8 2.8 0 0 0 19 28.8z" fill="#ffffff" fill-opacity=".2"/>')


def laptop():
    base = "M2.5 43.6h59l-2.4 6.6a2.4 2.4 0 0 1-2.2 1.6H7.1a2.4 2.4 0 0 1-2.2-1.6z"
    return (body(8, 7.5, 48, 37, 3.4) + glass(9, 8.5, 46, 35, 2.8) + screen(11, 10.5, 42, 31, 1)
            + reflection(9, 8.5, 46, 35, 2.8) + '<rect x="30.6" y="9.2" width="2.8" height=".9" rx=".45" fill="#2b2d33"/>'
            + solid(base, "lip") + '<path d="M3 44.1h58" stroke="#ffffff" stroke-width=".7"/>'
            + deboss(rr(26.5, 43.8, 11, 2, 1)))


def display():
    neck = "M26.6 42h10.8l2.8 11H23.8z"
    return (solid(neck, "alu-dark") + '<path d="M26.6 42h10.8l.6 2.4H26z" fill="#000000" fill-opacity=".22"/>'
            + body(17, 51.6, 30, 4.8, 2.4) + body(4, 5, 56, 39, 3, "graphite") + glass(5, 6, 54, 37, 2.4)
            + screen(7.6, 8.6, 48.8, 31.8, .8) + reflection(5, 6, 54, 37, 2.4))


def phone():
    return (body(18.5, 3, 27, 55, 7.6, "graphite") + glass(20, 4.5, 24, 52, 6.3) + screen(21.4, 5.9, 21.2, 49.2, 5.1)
            + '<rect x="28.2" y="8.6" width="7.6" height="2.6" rx="1.3" fill="#000000"/>' + reflection(20, 4.5, 24, 52, 6.3)
            + '<rect x="17.6" y="17" width="1.2" height="6" rx=".6" fill="#3a3c41"/><rect x="45.2" y="20" width="1.2" height="9" rx=".6" fill="#3a3c41"/>')


def ebook():
    lines = "".join(f'<path d="M21.6 {14.2 + i * 4}h{20.8 - (8 if i == 6 else 0)}" stroke="#8f8c82" stroke-opacity=".75" '
                    f'stroke-width="1.2" stroke-linecap="round"/>' for i in range(7))
    paper = rr(18.5, 8, 27, 39, 1.2)
    return (body(14.5, 3.5, 35, 54, 5.2, "graphite")
            + f'<path d="{paper}" fill="#e9e7e0" filter="url(#inset)"/>' + lines
            + '<path d="M21.6 10.6h4M38.4 10.6h4" stroke="#8f8c82" stroke-width=".7" stroke-linecap="round"/>'
            + '<path d="M21.6 44h20.8" stroke="#c9c6bc" stroke-width=".9" stroke-linecap="round"/>'
            + '<path d="M21.6 44h7.6" stroke="#5c5a54" stroke-width=".9" stroke-linecap="round"/>'
            + reflection(18.5, 8, 27, 39, 1.2) + deboss(rr(28, 50.5, 8, 1.8, .9), "#3a3c41"))


def drawing_tablet():
    pen = ('<path d="M21.6 46.6 48.4 17.6" stroke="#000000" stroke-opacity=".25" stroke-width="4.4" stroke-linecap="round" filter="url(#soft)"/>'
           '<path d="M22 46 48 18" stroke="#c9cbd0" stroke-width="3.6" stroke-linecap="round"/>'
           '<path d="M22 46 48 18" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round"/>'
           '<path d="M22 46l2.4-2.6" stroke="#4a4d53" stroke-width="3.2" stroke-linecap="round"/>')
    area = rr(13, 17.5, 43, 22.5, 2)
    keys = "".join(deboss(rr(6, 18 + i * 5.4, 3.6, 4.2, 1), "#3a3c41") for i in range(4))
    return (body(3, 13, 58, 33, 5, "graphite") + lip(3, 40.5, 58, 5.5, "lip-dark") + keys
            + f'<path d="{area}" fill="#111214" filter="url(#inset)"/>'
            + "".join(f'<path d="M{x} {y}h{dx}M{x} {y}v{dy}" stroke="#5c5f66" stroke-width=".6" stroke-linecap="round"/>'
                      for x, y, dx, dy in ((15, 19.5, 2, 2), (54, 19.5, -2, 2), (15, 38, 2, -2), (54, 38, -2, -2)))
            + reflection(13, 17.5, 43, 22.5, 2) + led(57.6, 17.6, "#5ac8fa") + pen)


def keyboard():
    keys, y = [], 22.6
    for h, n, wide in [(2.4, 14, None), (3.8, 13, "tail"), (3.8, 13, "head"), (3.8, 12, "both"), (3.8, 9, "space")]:
        unit = (52.4 - .9 * (n - 1)) / n
        widths = [unit] * n
        if wide == "space":
            widths = [unit] * 3 + [unit * 3 + 1.8] + [unit] * 3
        elif wide == "tail":
            widths[-1] += unit * .5; widths[0] -= unit * .5
        elif wide == "head":
            widths[0] += unit * .5; widths[-1] -= unit * .5
        elif wide == "both":
            widths[0] += unit * .7; widths[-1] += unit * .7
        scale = 52.4 / (sum(widths) + .9 * (len(widths) - 1))
        x = 5.8
        for w in widths:
            w *= scale
            keys.append(f'<path d="{rr(x - .15, y - .15, w + .3, h + .5, .8)}" fill="#8b8d92" fill-opacity=".55"/>'
                        f'<path d="{rr(x, y, w, h, .75)}" fill="url(#plastic)"/>')
            x += w + .9
        y += h + .9
    return body(3, 20, 58, 25, 3.6) + lip(3, 40.2, 58, 4.8) + "".join(keys)


def mouse():
    top = rr(20, 5, 24, 48, 12)
    return (body(20.6, 8.4, 22.8, 47.6, 11.4, "alu-dark") + solid(top, "plastic")
            + '<ellipse cx="27.4" cy="16" rx="3.2" ry="8" fill="#ffffff" fill-opacity=".9" filter="url(#soft)"/>'
            + '<path d="M22 40a10 10 0 0 0 20 0" fill="none" stroke="#000000" stroke-opacity=".05" stroke-width="3" filter="url(#soft)"/>'
            + '<path d="M32 5.6v17.4M20.6 23h22.8" stroke="#b5b8be" stroke-width=".5"/>'
            + '<rect x="30.2" y="9.6" width="3.6" height="8.4" rx="1.8" fill="url(#graphite)" filter="url(#inset)"/>'
            + '<path d="M31 11.4h2M31 13h2M31 14.6h2M31 16.2h2" stroke="#ffffff" stroke-opacity=".25" stroke-width=".5"/>')


def gamepad():
    d = ("M20 15h24c6.5 0 9.6 3.6 11.4 9.4l3.6 12.4c1.5 5.2-3.2 9.3-7.8 6.6L45 39H19l-6.2 4.4"
         "c-4.6 2.7-9.3-1.4-7.8-6.6l3.6-12.4C10.4 18.6 13.5 15 20 15z")
    buttons = "".join(deboss(ring(x, y, 2.1, .01), color) for (x, y), color in zip(((45, 21), (49, 25), (45, 29), (41, 25)),
                                          ("#ffd60a", "#ff453a", "#30d158", "#0a84ff")))
    sticks = "".join(f'<circle cx="{x}" cy="33" r="4.4" fill="#000000" fill-opacity=".3" filter="url(#soft)"/>'
                     f'<circle cx="{x}" cy="32.6" r="3.9" fill="url(#cone)"/>'
                     f'<circle cx="{x}" cy="32.6" r="2.5" fill="none" stroke="#ffffff" stroke-opacity=".16" stroke-width=".6"/>'
                     for x in (25, 39))
    return (solid(d, "graphite") + deboss("M17.6 20.4h3.2v3.2h3.2v3.2h-3.2v3.2h-3.2v-3.2h-3.2v-3.2h3.2z", "#55585f")
            + buttons + sticks)


def headphones(mic=False):
    band = ('<path d="M14.6 30V25a17.4 17.4 0 0 1 34.8 0v5" fill="none" stroke="#7d7f85" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M14.6 30V25a17.4 17.4 0 0 1 34.8 0v5" fill="none" stroke="#e8e9ec" stroke-width="3.8" stroke-linecap="round"/>'
            '<path d="M14.2 28V25a17.8 17.8 0 0 1 35.6 0v3" fill="none" stroke="#ffffff" stroke-width=".8" stroke-linecap="round"/>'
            '<path d="M18 28.4V25.6a14 14 0 0 1 28 0v2.8" fill="none" stroke="url(#mesh)" stroke-width="2.6" stroke-linecap="round"/>')
    cups = ""
    for x, cx in ((6, 19.2), (43, 40.8)):
        cushion = rr(cx - 3.2, 30.4, 6.4, 20.4, 3.2)
        cups += (body(x, 28, 15, 25, 6.8, "graphite") + f'<path d="{cushion}" fill="url(#graphite)"/>'
                 + f'<path d="{cushion}" fill="url(#mesh-light)" fill-opacity=".35"/><path d="{cushion}" fill="url(#side)"/>')
    boom = ('<path d="M12 52c1 4.4 6 5.4 13 5.4" fill="none" stroke="#7d7f85" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M12 52c1 4.4 6 5.4 13 5.4" fill="none" stroke="#eceef1" stroke-width="1.6" stroke-linecap="round"/>'
            '<rect x="23.6" y="55.2" width="6.8" height="4.2" rx="2.1" fill="url(#cone)"/>') if mic else ""
    return band + cups + boom


def speaker():
    woofer = (f'<path fill-rule="evenodd" d="{ring(32, 35, 12.6, 11)}" fill="#ffffff" fill-opacity=".7" filter="url(#soft)"/>'
              '<circle cx="32" cy="35" r="11" fill="url(#cone)" filter="url(#inset)"/>'
              '<circle cx="32" cy="35" r="11" fill="url(#mesh)" fill-opacity=".6"/>'
              '<circle cx="32" cy="35" r="3.8" fill="#2a2c31"/><circle cx="31" cy="34" r="1.6" fill="#ffffff" fill-opacity=".14"/>')
    tweeter = ('<circle cx="32" cy="15.4" r="4.6" fill="url(#cone)" filter="url(#inset)"/>'
               '<circle cx="31.2" cy="14.6" r="1.4" fill="#ffffff" fill-opacity=".2"/>')
    return drive(13.5, 4, 37, 54, "graphite", "lip-dark") + woofer + tweeter


def webcam():
    clip = "M26 36h12v4h7a2 2 0 0 1 2 2v3H17v-3a2 2 0 0 1 2-2h7z"
    return (solid(clip, "alu-dark") + body(12, 16, 40, 21, 10.5, "graphite")
            + '<circle cx="32" cy="26.5" r="8.4" fill="url(#steel)"/><circle cx="32" cy="26.5" r="7" fill="#08090b"/>'
            + '<circle cx="32" cy="26.5" r="4.4" fill="url(#lens)"/><circle cx="32" cy="26.5" r="2" fill="#0a1022"/>'
            + '<ellipse cx="30.4" cy="24.8" rx="1.3" ry=".9" fill="#ffffff" fill-opacity=".75"/>'
            + '<circle cx="44.6" cy="26.5" r="1" fill="#30d158"/><circle cx="44.6" cy="26.5" r="1.8" fill="#30d158" fill-opacity=".25" filter="url(#soft)"/>')


def microphone():
    capsule = rr(22, 3.5, 20, 30.5, 10)
    yoke = ('<path d="M18.5 20v5a13.5 13.5 0 0 0 27 0v-5" fill="none" stroke="#7d7f85" stroke-width="3.2" stroke-linecap="round"/>'
            '<path d="M18.5 20v5a13.5 13.5 0 0 0 27 0v-5" fill="none" stroke="#e8e9ec" stroke-width="2.2" stroke-linecap="round"/>')
    return (body(30.6, 38, 2.8, 14, 1.2, "steel") + yoke + solid(capsule, "alu-dark")
            + f'<path d="{capsule}" fill="url(#mesh)" fill-opacity=".7"/><path d="{capsule}" fill="url(#side)"/>'
            + body(21.6, 21.6, 20.8, 3.4, 1.7, "steel") + body(18.5, 47, 27, 8, 3) + lip(18.5, 50.5, 27, 4.5))


def printer():
    paper = "M15 33.6h34l1.8 13.6H13.2z"
    return (body(17, 3.5, 30, 16, .6, "plastic") + '<path d="M18 12h28" stroke="#c9ccd2" stroke-width=".6"/>'
            + body(5, 15, 54, 30, 5, "plastic") + lip(5, 39.5, 54, 5.5, "lip-white")
            + deboss(rr(13, 31, 38, 2.6, 1.3), "#24262b") + glass(43, 20, 10, 4.6, 1.2) + reflection(43, 20, 10, 4.6, 1.2)
            + '<circle cx="11" cy="22.4" r="1" fill="#30d158"/>'
            + f'<path d="{paper}" fill="#000000" fill-opacity=".18" filter="url(#soft)"/>' + solid(paper, "plastic")
            + '<path d="M18 38.4h20M17.6 41.8h26" stroke="#aeb1b8" stroke-width=".9" stroke-linecap="round"/>')


def scanner():
    lid = "M10 18h44a3 3 0 0 1 2.8 1.9L60 28H4l3.2-8.1A3 3 0 0 1 10 18z"
    return (solid(lid, "plastic") + deboss(rr(16, 22, 32, 2.2, 1.1), "#e0e2e6")
            + body(4, 28, 56, 17, 3.6, "graphite") + lip(4, 39.6, 56, 5.4, "lip-dark")
            + '<rect x="7" y="28.6" width="50" height="1.6" rx=".8" fill="#7fe3ff"/>'
            + '<rect x="7" y="27.6" width="50" height="3.6" rx="1.8" fill="#7fe3ff" fill-opacity=".35" filter="url(#soft)"/>'
            + "".join(deboss(rr(9 + i * 6, 34.2, 4.4, 2.4, 1.2), "#3a3c41") for i in range(3))
            + deboss(ring(53, 35.4, 1.6, .01), "#3a3c41") + led(48.4, 35.4))


def sim():
    d = "M19 6h21l8 8v40a3 3 0 0 1-3 3H19a3 3 0 0 1-3-3V9a3 3 0 0 1 3-3z"
    chip = rr(21, 22, 22, 18, 3.4)
    return (solid(d, "plastic") + f'<path d="{chip}" fill="url(#gold)"/><path d="{chip}" fill="url(#bevel)"/>'
            + '<path d="M21 31h22M32 22v18M21 26.5h7M36 26.5h7M21 35.5h7M36 35.5h7" stroke="#9a7428" stroke-width=".7"/>')


def battery():
    wrap = rr(21, 15, 22, 43, 4.5)
    return (body(28, 6, 8, 6, 1.5, "steel") + body(21, 10, 22, 48, 4.5, "steel") + solid(wrap, "green")
            + deboss("M31 21h2v3h3v2h-3v3h-2v-3h-3v-2h3z", "#1d8a35") + deboss(rr(28, 44, 8, 2, 1), "#1d8a35"))


def bluetooth(fig):
    return body(17, 10, 30, 44, 9, "plastic") + lip(17, 47, 30, 7, "lip-white") + emblem(32, 27, 10, fig) + led(32, 42.5, "#0a84ff")


def camera_photo():
    lens = ('<circle cx="32" cy="37" r="13.2" fill="url(#steel)"/><circle cx="32" cy="37" r="11.2" fill="#08090b"/>'
            '<circle cx="32" cy="37" r="7.6" fill="url(#lens)"/><circle cx="32" cy="37" r="3" fill="#0a1022"/>'
            '<ellipse cx="29" cy="34" rx="2.4" ry="1.6" fill="#ffffff" fill-opacity=".7"/>')
    return (body(13, 12, 15, 9, 2, "alu") + body(43, 14, 9, 6, 2, "steel") + body(5, 18, 54, 36, 5)
            + '<rect x="5" y="27" width="54" height="20" fill="url(#graphite)"/><rect x="5" y="27" width="54" height="20" fill="url(#mesh-light)" fill-opacity=".15"/>'
            + '<rect x="5" y="27" width="54" height="20" fill="url(#side)"/>'
            + glass(9, 21, 9, 4, 1) + '<rect x="10" y="21.8" width="7" height="2.4" rx=".6" fill="#ffffff" fill-opacity=".55"/>'
            + lens + led(52, 23, "#ff9f0a"))


def camera_video():
    panel = rr(2, 23, 13, 18, 2)
    return (body(12, 15, 13, 8, 2, "graphite") + body(8, 20, 38, 26, 6, "graphite")
            + body(44, 23, 15, 20, 3, "graphite") + '<ellipse cx="58" cy="33" rx="2.2" ry="8" fill="url(#lens)"/>'
            + '<ellipse cx="57.6" cy="30" rx=".8" ry="2.4" fill="#ffffff" fill-opacity=".6"/>'
            + solid(panel, "graphite") + f'<path d="{rr(3.4, 24.4, 10.2, 15.2, 1.2)}" fill="url(#crystal)"/>'
            + reflection(3.4, 24.4, 10.2, 15.2, 1.2) + led(20, 27, "#ff453a")
            + "".join(deboss(rr(24 + i * 5, 38, 3.4, 2, 1), "#3a3c41") for i in range(3)))


def cpu():
    pins = "".join(f'<rect x="{12.5 + i * 4}" y="{y}" width="2" height="1.2" rx=".3" fill="url(#gold)"/>'
                   for i in range(10) for y in (8.6, 54.2))
    return (body(6, 6, 52, 52, 4, "pcb") + pins + '<path d="M9 9h5l-5 5z" fill="url(#gold)"/>'
            + body(14, 14, 36, 36, 4) + deboss(rr(20, 40, 24, 2.4, 1.2)) + deboss(rr(20, 20, 10, 2.4, 1.2)))


def memory():
    board = "M4.6 20h54.8a1.6 1.6 0 0 1 1.6 1.6V42H36v-2.6h-3V42H3V21.6A1.6 1.6 0 0 1 4.6 20z"
    fingers = "".join(f'<rect x="{4.4 + i * 2.1:.1f}" y="38.4" width="1.3" height="3.4" fill="url(#gold)"/>'
                      for i in range(27) if not 30.6 < 4.4 + i * 2.1 < 36.4)
    chips = "".join(body(6.6 + i * 13.2, 24, 11, 11, .8, "graphite") for i in range(4))
    return solid(board, "pcb") + fingers + chips


def network_card():
    board = "M10 14h46a1.6 1.6 0 0 1 1.6 1.6V42H52v4.4H22V42H10z"
    fingers = "".join(f'<rect x="{23.2 + i * 2.1:.1f}" y="42.6" width="1.3" height="3.6" fill="url(#gold)"/>' for i in range(14))
    return (body(4, 8, 6, 46, 1, "steel") + solid(board, "pcb") + fingers
            + body(10, 18, 11, 13, 1, "graphite") + '<rect x="12" y="21" width="7" height="5" rx=".6" fill="#08090b"/>'
            + '<path d="M13.2 21.4v1.8M14.6 21.4v1.8M16 21.4v1.8M17.4 21.4v1.8" stroke="#d6ae55" stroke-width=".5"/>'
            + body(32, 20, 14, 14, 1.2, "graphite") + led(14, 36) + led(18, 36, "#ff9f0a"))


def media_cf():
    holes = "".join(f'<circle cx="{15.6 + i * 2.8:.1f}" cy="{y}" r=".55" fill="#08090b"/>' for i in range(12) for y in (10.4, 12.6))
    label = rr(15, 17, 34, 34, 2)
    return (body(12, 7, 40, 48, 2.6, "graphite") + holes
            + f'<path d="{label}" fill="url(#label)"/><path d="{label}" fill="url(#bevel)"/>'
            + '<path d="M32 22l3.4 4.4h-6.8z" fill="#ffffff"/>')


def media_ms():
    contacts = "".join(f'<rect x="6.4" y="{23.2 + i * 1.9:.1f}" width="3.6" height="1.1" rx=".3" fill="url(#gold)"/>' for i in range(10))
    label = rr(15, 23.5, 41, 17, 1.6)
    return (body(4, 20, 56, 24, 2, "graphite") + contacts + f'<path d="{label}" fill="url(#plastic)"/>'
            + '<rect x="15" y="23.5" width="41" height="4" fill="url(#label)"/>'
            + '<path d="M19 33h24M19 36.4h16" stroke="#a9acb3" stroke-width="1" stroke-linecap="round"/>')


def media_sm():
    d = "M14 6h30l6 6v43a2 2 0 0 1-2 2H14a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z"
    plate, label = rr(19, 13, 24, 19, 2), rr(16, 38, 30, 14, 1.6)
    return (solid(d, "plastic") + f'<path d="{plate}" fill="url(#gold)"/><path d="{plate}" fill="url(#bevel)"/>'
            + '<path d="M19 19.3h24M19 25.6h24M31 13v19" stroke="#9a7428" stroke-width=".7"/>'
            + f'<path d="{label}" fill="url(#label)"/><path d="{label}" fill="url(#bevel)"/>')


def dialpad():
    keys = "".join(deboss(rr(17.4 + c * 10.4, 9 + r * 11.6, 8.4, 9.2, 3.2), "#d4d6db") for c in range(3) for r in range(4))
    return body(12, 3, 40, 56, 7, "plastic") + lip(12, 52, 40, 7, "lip-white") + keys


def touchpad():
    return body(4, 13, 56, 36, 5) + f'<path d="{rr(6.4, 15.4, 51.2, 26.6, 3.4)}" fill="#e2e4e7" filter="url(#inset)"/>' + lip(4, 43, 56, 6)


def touchscreen():
    touch = ('<circle cx="35" cy="31" r="8" fill="#ffffff" fill-opacity=".18"/><circle cx="35" cy="31" r="5" fill="#ffffff" fill-opacity=".3"/>'
             '<circle cx="35" cy="31" r="2.6" fill="#ffffff" fill-opacity=".9"/>')
    return (body(5, 8, 54, 46, 5, "graphite") + glass(6.5, 9.5, 51, 43, 3.6) + screen(9, 12, 46, 38, 1.4) + touch
            + reflection(6.5, 9.5, 51, 43, 3.6))


def tvremote():
    buttons = "".join(deboss(circle(x, y, 1.9), "#4a4c52") for x in (28, 36) for y in (29, 35))
    return (body(24, 3, 16, 58, 8, "graphite") + solid(circle(32, 16, 6.6), "alu-dark")
            + '<circle cx="32" cy="16" r="2.6" fill="url(#graphite)"/>' + buttons
            + deboss(rr(29.6, 41, 4.8, 13, 2.4), "#4a4c52") + led(32, 8, "#ff453a"))


def player():
    arrows = ('<path d="M24.6 44l2.4-1.6v3.2zM39.4 44 37 42.4v3.2zM32 36.4l-1.4 2h2.8zM31 50.6h2" fill="#5c5f66" '
              'stroke="#5c5f66" stroke-width=".6" stroke-linejoin="round"/>')
    return (body(18, 3, 28, 57, 6, "graphite") + glass(20.5, 6, 23, 23, 2.4) + screen(22, 7.5, 20, 20, 1.2)
            + reflection(20.5, 6, 23, 23, 2.4) + solid(circle(32, 44, 10.4), "alu") + arrows
            + deboss(circle(32, 44, 4), "#c3c5c9"))


def router():
    antennas = body(12, 6, 3.6, 30, 1.8, "graphite") + body(48.4, 6, 3.6, 30, 1.8, "graphite")
    lights = "".join(led(16 + i * 5.2, 38.4) for i in range(5))
    return (antennas + body(6, 29, 52, 22, 5, "plastic") + lip(6, 44.6, 52, 6.4, "lip-white") + lights
            + deboss(rr(44, 37.4, 9, 2, 1), "#d4d6db"))


def jack(pins):
    w = 4 + pins * 2.2
    socket = rr(32 - w / 2, 20, w, 22, 2)
    contacts = "".join(f'<rect x="{32 - (pins - 1) * 1.1 + i * 2.2 - .45:.2f}" y="21.6" width=".9" height="7" fill="url(#gold)"/>'
                       for i in range(pins))
    return (body(10, 5, 44, 54, 6, "plastic") + f'<path d="{socket}" fill="#151618" filter="url(#inset)"/>' + contacts
            + f'<rect x="{32 - w / 4:.1f}" y="38" width="{w / 2:.1f}" height="4" fill="#2a2c31"/>' + screw(32, 11) + screw(32, 53))


def access_point(fig):
    return (body(18, 5, 28, 53, 10, "plastic") + lip(18, 50, 28, 8, "lip-white")
            + f'<g transform="translate(23 16) scale(1.125)"><path d="{fig}" fill="none" stroke="#1e9bf5" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/></g>' + led(32, 40))


def nas(fig):
    bays = "".join(body(x, 13, 17, 32, 2, "alu-dark") + deboss(rr(x + 3, 40, 11, 1.8, .9), "#7d7f85") + led(x + 8.5, 17)
                   for x in (14, 33))
    return body(10, 8, 44, 50, 5, "graphite") + lip(10, 51, 44, 7, "lip-dark") + bays + badge(fig)


def television():
    feet = solid("M13 46l-4.4 10h4.4l5-10z", "alu-dark") + solid("M51 46l4.4 10H51l-5-10z", "alu-dark")
    return (feet + body(2, 8, 60, 40, 2.6, "graphite") + glass(3, 9, 58, 38, 2) + screen(4.4, 10.4, 55.2, 35.2, .6)
            + reflection(3, 9, 58, 38, 2))


FLAME = "M8 2.5c.4 2.6 3.8 4.2 3.8 7.4a3.8 3.8 0 0 1-7.6 0c0-1.5.7-2.5 1.6-3.3.1 1.3.6 2 1.3 2.3C6.8 6.9 7.2 4.7 8 2.5z"
PARTITION = (-90, 30, "#1e9bf5")


def trash(full=False, dark=False):
    """A frosted, translucent bin seen slightly from above, after the macOS Trash."""
    k = "-dark" if dark else ""
    body = "M9 11a23 4.2 0 0 0 46 0l-4.4 43.6a5 5 0 0 1-5 4.4H18.4a5 5 0 0 1-5-4.4z"
    inside = ('<g filter="url(#haze)" opacity=".9"><ellipse cx="25" cy="30" rx="9" ry="12" fill="#ffffff"/>'
              '<ellipse cx="39" cy="26" rx="7" ry="9" fill="#7cc4ff"/><ellipse cx="33" cy="44" rx="10" ry="7" fill="#ffd76a"/>'
              '<ellipse cx="42" cy="47" rx="5" ry="6" fill="#ff8a7a"/></g>') if full else ""
    papers = ('<path d="M14 12c0-5 5-8.4 10-6.6 3-4.6 9.6-3.6 11.4.6 2.6-.8 5 0 6.4 1.6 3.4-.6 7.4 1.6 8.2 4.4z" fill="#ffffff"/>'
              '<path d="M38 7.4 46 4l3 6.6-8 2.4z" fill="#6fb7ff"/><path d="M38 7.4l8-3.4" stroke="#ffffff" stroke-opacity=".6" stroke-width=".6"/>'
              '<rect x="14" y="11" width="36" height="5" fill="#ffffff"/>'
              '<path d="M15.4 9c3 0 5 1.4 6 3.6M30.6 5c-1.6 1.8-1.8 4.4-.6 7.2M23.6 5.8c.8 1.2 1 2.8.6 4.4" '
              'fill="none" stroke="#b9bdc5" stroke-width=".7" stroke-linecap="round"/>') if full else ""
    return (f'<ellipse cx="32" cy="11" rx="23" ry="4.2" fill="url(#bin-inside{k})"/>' + inside + papers
            + f'<path d="{body}" fill="url(#bin{k})"/><path d="{body}" fill="url(#side)"/><path d="{body}" fill="url(#frost)"/>'
            + f'<ellipse cx="32" cy="11" rx="23" ry="4.2" fill="none" stroke="#ffffff" stroke-opacity="{.35 if dark else .9}" stroke-width=".9"/>'
            + f'<path d="M15 55.4a17 3.2 0 0 0 34 0" fill="none" stroke="#000000" stroke-opacity=".08" stroke-width="1.2"/>')


def trash_icons(dark=False):
    return {"user-trash": wrap(trash(dark=dark)), "user-trash-full": wrap(trash(full=True, dark=dark))}


def server():
    units = "".join(body(18, 9 + i * 10.5, 28, 8, 1.4, "alu-dark") + deboss(rr(22, 12.4 + i * 10.5, 14, 1.6, .8), "#7d7f85")
                    + led(41, 13 + i * 10.5) for i in range(4))
    return body(14, 4, 36, 54, 4, "graphite") + lip(14, 51, 36, 7, "lip-dark") + units


def globe():
    grid = ('<g fill="none" stroke="#ffffff" stroke-opacity=".38" stroke-width=".8">'
            '<ellipse cx="32" cy="32" rx="10" ry="24"/><path d="M32 8v48M8 32h48M11 20h42M11 44h42"/></g>')
    return ('<circle cx="32" cy="32" r="24.5" fill="url(#globe)"/>' + grid
            + '<ellipse cx="24" cy="19" rx="10" ry="6" fill="#ffffff" fill-opacity=".45" filter="url(#soft)" transform="rotate(-30 24 19)"/>'
            + '<circle cx="32" cy="32" r="24.5" fill="none" stroke="#0b3e9c" stroke-opacity=".35" stroke-width=".6"/>')


def floppy():
    shutter = "M22 4h22v17a2 2 0 0 1-2 2H24a2 2 0 0 1-2-2z"
    return (solid("M9 4h43l5 5v46a3 3 0 0 1-3 3H10a3 3 0 0 1-3-3V6a2 2 0 0 1 2-2z", "graphite")
            + solid(shutter, "steel") + '<rect x="35" y="7" width="5" height="12" rx="1" fill="#2c2e33"/>'
            + f'<path d="{rr(13, 30, 38, 26, 2)}" fill="url(#plastic)"/>'
            + '<rect x="13" y="30" width="38" height="4" fill="url(#label)"/>'
            + '<path d="M17 40h28M17 45h28M17 50h18" stroke="#a9acb3" stroke-width="1" stroke-linecap="round"/>'
            + deboss(rr(9.4, 53, 3, 3, .6), "#0e0f11"))


def picture():
    return (body(5, 11, 54, 42, 4, "plastic") + f'<path d="{rr(9.5, 15.5, 45, 33, 1.6)}" fill="#d5d8de" filter="url(#inset)"/>'
            + '<circle cx="43" cy="24" r="3.6" fill="#c0c4cb"/>'
            + '<path d="M9.5 46.9 22 31l8 10 6-7 18.5 13.4v-.3a1.6 1.6 0 0 1-1.6 1.6H11.1z" fill="#aeb2ba"/>')


def avatar():
    return ('<clipPath id="face"><circle cx="32" cy="32" r="26"/></clipPath>'
            '<circle cx="32" cy="32" r="26" fill="url(#alu-dark)"/>'
            '<g clip-path="url(#face)" fill="#ffffff" fill-opacity=".92"><circle cx="32" cy="25" r="9.5"/>'
            '<ellipse cx="32" cy="56" rx="19" ry="16"/></g>'
            '<circle cx="32" cy="32" r="26" fill="url(#bevel)"/>')


def status(glyph):
    """Status icons drawn as objects."""
    return {name: wrap(art) for name, art in {
        "avatar-default": avatar(), "image-missing": picture() + badge(glyph("exclaim"), "#e0321f"),
        "image-loading": picture() + badge(glyph("clock"), "url(#graphite)")}.items()}


DEVICES = {
    "audio-card": speaker, "audio-headphones": headphones, "audio-headset": lambda: headphones(mic=True),
    "camera-web": webcam, "computer": laptop, "drive-harddisk": harddisk, "drive-multidisk": multidisk,
    "drive-optical": optical_drive, "drive-removable-media": removable_drive, "ebook-reader": ebook,
    "input-gaming": gamepad, "input-keyboard": keyboard, "input-mouse": mouse, "input-tablet": drawing_tablet,
    "media-flash": sd_card, "media-optical": optical_disc, "media-removable": usb_stick,
    "microphone": microphone, "phone": phone, "printer": printer, "scanner": scanner, "video-display": display,
    "audio-input-microphone": microphone, "audio-speakers": speaker, "auth-sim": sim, "battery": battery,
    "camera-photo": camera_photo, "camera-video": camera_video, "computer-laptop": laptop, "cpu": cpu,
    "device-harddisk-usb": removable_drive, "drive-removable-media-usb": usb_stick,
    "drive-partition": lambda: harddisk((PARTITION,)),
    "drive-multipartition": lambda: harddisk((PARTITION, (30, 140, "#ff9f0a"), (140, 215, "#30d158"))),
    "gnome-dev-media-cf": media_cf, "gnome-dev-media-ms": media_ms, "gnome-dev-media-sdmmc": sd_card,
    "gnome-dev-media-sm": media_sm, "input-dialpad": dialpad, "input-touchpad": touchpad,
    "input-touchscreen": touchscreen, "input-tvremote": tvremote, "memory": memory, "modem": router,
    "multimedia-player": player, "network-card": network_card, "network-modem": router,
    "network-rj11-female": lambda: jack(4), "network-rj45-female": lambda: jack(8), "network-wired": lambda: jack(8),
    "video-television": television, "media-floppy": floppy,
}


def discs(glyph, label):
    ink = "#7d8088"
    cd = optical_disc() + label("CD", 30.4, 40.6, 5.4, ink) + label("R", 38.4, 42.6, 3.4, ink)
    dvd = optical_disc() + label("DVD", 32, 40.6, 5.4, ink)
    return {"media-cdr": cd, "media-dvd": dvd, "media-write-cd": cd + emblem(51, 51, 9, FLAME, "url(#graphite)"),
            "media-write-dvd": dvd + emblem(51, 51, 9, FLAME, "#8e44d6"),
            "media-cdrom-audio": optical_disc() + f'<g transform="translate(26.4 38) scale(.7)"><path d="{glyph("note")}" '
            f'fill="none" stroke="{ink}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></g>'}


def wrap(art):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 64 64">'
            f'<defs>{DEFS}</defs><g filter="url(#drop)">{art}</g></svg>\n')


def places():
    """The places drawn as objects rather than folders."""
    return {**trash_icons(), "network-server": wrap(server()), "network-workgroup": wrap(globe())}


def icons(glyph, label):
    """name → SVG for every device; `glyph(name)` returns the `d` of a symbolic source and
    `label(text, cx, top, height, color)` draws stroked letters."""
    out = {name: draw() for name, draw in DEVICES.items()}
    out.update(discs(glyph, label))
    out["printer-network"] = printer() + badge(glyph("network-wireless"))
    out["gnome-dev-printer-new"] = printer() + badge(glyph("list-add"), "url(#green)")
    out["drive-harddisk-root"] = harddisk() + badge(glyph("emblem-system"))
    out["bluetooth"] = bluetooth(glyph("bluetooth"))
    out["network-wireless"] = access_point(glyph("network-wireless"))
    out["network_fs"] = nas(glyph("network-workgroup"))
    return {name: wrap(art) for name, art in sorted(out.items())}
