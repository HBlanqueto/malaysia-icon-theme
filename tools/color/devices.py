"""Device icons rendered like macOS hardware icons.

Apple's guidance for macOS icons asks for lifelike rendering: a front-facing, level view,
one consistent drop shadow, and objects that look made of physical materials with mass.
Edges come from light, never from an outline. The reference is the macOS 26.1 drive icon:
aluminum with rounded, cylindrically lit sides, a beveled top edge, a rounded bottom face
with its own volume, and marks pressed into the metal with a soft inner shadow.
"""

DEFS = (
    # one drop shadow for every device: a soft cast shadow plus a tight contact shadow
    '<filter id="drop" x="-25%" y="-25%" width="150%" height="160%">'
    '<feGaussianBlur in="SourceAlpha" stdDeviation="1.6"/><feOffset dy="1.8" result="far"/>'
    '<feFlood flood-color="#000000" flood-opacity=".26"/><feComposite in2="far" operator="in" result="cast"/>'
    '<feGaussianBlur in="SourceAlpha" stdDeviation=".35"/><feOffset dy=".45" result="near"/>'
    '<feFlood flood-color="#000000" flood-opacity=".3"/><feComposite in2="near" operator="in" result="contact"/>'
    '<feMerge><feMergeNode in="cast"/><feMergeNode in="contact"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    # a mark pressed into the surface: shadow inside its upper edge
    '<filter id="inset" x="-30%" y="-30%" width="160%" height="160%">'
    '<feComponentTransfer in="SourceAlpha"><feFuncA type="table" tableValues="1 0"/></feComponentTransfer>'
    '<feGaussianBlur stdDeviation=".55"/><feOffset dy=".7" result="edge"/>'
    '<feFlood flood-color="#000000" flood-opacity=".5"/><feComposite in2="edge" operator="in"/>'
    '<feComposite in2="SourceAlpha" operator="in" result="shade"/>'
    '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shade"/></feMerge></filter>'
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


def badge(fig):
    return ('<circle cx="51" cy="13" r="9" fill="#ffffff"/><circle cx="51" cy="13" r="7.8" fill="url(#label)"/>'
            '<circle cx="51" cy="13" r="7.8" fill="url(#bevel)"/>'
            f'<g transform="translate(44.6 6.6) scale(.8)"><path fill="none" stroke="#ffffff" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" d="{fig}"/></g>')


def drive(x, y, w, h, fill="alu"):
    """A body whose bottom face shows as a thin, darker band the full width of the body."""
    band = round(max(7, h * .14), 1)
    return body(x, y, w, h, round(max(3.6, w * .12), 1), fill) + lip(x, y + h - band, w, band)


def screw(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="1.3" fill="url(#steel)" filter="url(#inset)"/>'
            f'<path d="M{cx - .7} {cy}h1.4" stroke="#5c5f66" stroke-width=".45"/>')


def harddisk():
    """An open 3.5-inch drive seen from above: platter, spindle, actuator arm and label."""
    platter = ring(32, 25, 19, 4.6)
    arm = "M46.6 47.6 35.4 31.6a1.3 1.3 0 0 1 2-1.5l12.8 15.2z"
    label = rr(13.5, 48, 22, 8.6, 1.2)
    return (body(9, 3, 46, 57, 4) + deboss(rr(11.4, 5.4, 41.2, 52.2, 2.6), "#c3c5c9")
            + f'<path fill-rule="evenodd" d="{ring(32, 25, 19.8, 19)}" fill="#000000" fill-opacity=".25" filter="url(#soft)"/>'
            + f'<path fill-rule="evenodd" d="{platter}" fill="url(#platter)"/>'
            + f'<path fill-rule="evenodd" d="{platter}" fill="url(#sheen2)"/>'
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
    return cable + drive(8, 17, 42, 36) + deboss(ring(29, 31, 5.8, 2))


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
            + drive(21, 14, 22, 44) + deboss(ring(32, 45.5, 2.6, 1.6)))


def sd_card():
    d = "M18 6h22l9 9v39a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V9a3 3 0 0 1 3-3z"
    contacts = "".join(f'<rect x="{19.2 + i * 3.6:.1f}" y="8.4" width="2.4" height="8.4" rx=".7" fill="url(#gold)"/>'
                       for i in range(6))
    label = rr(19, 26, 26, 25, 2.8)
    return (solid(d, "plastic") + contacts + deboss(rr(13.4, 29, 2.2, 9, .9), "#d3d5da")
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
            + body(17, 51.6, 30, 4.8, 2.4) + body(4, 5, 56, 39, 3) + glass(5, 6, 54, 37, 2.4)
            + screen(7.6, 8.6, 48.8, 31.8, .8) + reflection(5, 6, 54, 37, 2.4))


def phone():
    return (body(18.5, 3, 27, 55, 7.6, "steel") + glass(20, 4.5, 24, 52, 6.3) + screen(21.4, 5.9, 21.2, 49.2, 5.1)
            + '<rect x="28.2" y="8.6" width="7.6" height="2.6" rx="1.3" fill="#000000"/>' + reflection(20, 4.5, 24, 52, 6.3)
            + '<rect x="17.6" y="17" width="1.2" height="6" rx=".6" fill="#9a9ca2"/><rect x="45.2" y="20" width="1.2" height="9" rx=".6" fill="#9a9ca2"/>')


def ebook():
    lines = "".join(f'<path d="M21.6 {14.2 + i * 4}h{20.8 - (8 if i == 6 else 0)}" stroke="#8f8c82" stroke-opacity=".75" '
                    f'stroke-width="1.2" stroke-linecap="round"/>' for i in range(7))
    paper = rr(18.5, 8, 27, 39, 1.2)
    return (body(14.5, 3.5, 35, 54, 5.2, "plastic")
            + f'<path d="{paper}" fill="#e9e7e0" filter="url(#inset)"/>' + lines
            + deboss(rr(28, 50.5, 8, 1.8, .9), "#dcdee2"))


def drawing_tablet():
    pen = ('<path d="M21.6 46.6 48.4 17.6" stroke="#000000" stroke-opacity=".25" stroke-width="4.4" stroke-linecap="round" filter="url(#soft)"/>'
           '<path d="M22 46 48 18" stroke="#c9cbd0" stroke-width="3.6" stroke-linecap="round"/>'
           '<path d="M22 46 48 18" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round"/>'
           '<path d="M22 46l2.4-2.6" stroke="#4a4d53" stroke-width="3.2" stroke-linecap="round"/>')
    area = rr(9, 17.5, 46, 24.5, 2)
    return (body(3, 13, 58, 33, 5) + lip(3, 40.5, 58, 5.5) + f'<path d="{area}" fill="url(#glass)" filter="url(#inset)"/>'
            + reflection(9, 17.5, 46, 24.5, 2) + pen)


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
    return drive(13.5, 4, 37, 54) + woofer + tweeter


def webcam():
    clip = "M26 36h12v4h7a2 2 0 0 1 2 2v3H17v-3a2 2 0 0 1 2-2h7z"
    return (solid(clip, "alu-dark") + body(12, 16, 40, 21, 10.5)
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
            + body(4, 28, 56, 17, 3.6, "plastic") + lip(4, 39.6, 56, 5.4, "lip-white")
            + '<rect x="7" y="28.6" width="50" height="1.6" rx=".8" fill="#7fe3ff"/>'
            + '<rect x="7" y="27.6" width="50" height="3.6" rx="1.8" fill="#7fe3ff" fill-opacity=".35" filter="url(#soft)"/>'
            + deboss(ring(53, 36, 1.6, .01), "#d0d3d8") + '<circle cx="48.6" cy="36" r=".9" fill="#30d158"/>')


DEVICES = {
    "audio-card": speaker, "audio-headphones": headphones, "audio-headset": lambda: headphones(mic=True),
    "camera-web": webcam, "computer": laptop, "drive-harddisk": harddisk, "drive-multidisk": multidisk,
    "drive-optical": optical_drive, "drive-removable-media": removable_drive, "ebook-reader": ebook,
    "input-gaming": gamepad, "input-keyboard": keyboard, "input-mouse": mouse, "input-tablet": drawing_tablet,
    "media-flash": sd_card, "media-optical": optical_disc, "media-removable": usb_stick,
    "microphone": microphone, "phone": phone, "printer": printer, "scanner": scanner, "video-display": display,
}


def icons(glyph):
    """name → SVG for every device; `glyph(name)` returns the `d` of a symbolic source."""
    out = {name: draw() for name, draw in DEVICES.items()}
    out["printer-network"] = printer() + badge(glyph("network-wireless"))
    return {name: ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 64 64">'
                   f'<defs>{DEFS}</defs><g filter="url(#drop)">{art}</g></svg>\n') for name, art in sorted(out.items())}
