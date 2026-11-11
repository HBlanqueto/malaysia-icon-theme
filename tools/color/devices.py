"""Device icons in the style of current macOS hardware icons.

Every device is drawn from the same few materials (silver aluminum with cylindrical side
shading, white plastic, black glass, a bold wallpaper) seen almost straight on, with the
bottom face showing as a darker lip and a soft contact shadow. Detail is kept to debossed
marks, as in the macOS 26.1 drive icon.
"""

INK_EDGE = 'stroke="#000000" stroke-opacity=".26" stroke-width=".6"'

DEFS = (
    '<linearGradient id="alu" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#f2f3f5"/><stop offset=".55" stop-color="#d3d5d9"/><stop offset="1" stop-color="#b3b5ba"/></linearGradient>'
    '<linearGradient id="alu-dark" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#d6d8dc"/><stop offset="1" stop-color="#9c9ea3"/></linearGradient>'
    '<linearGradient id="side" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#000000" stop-opacity=".22"/><stop offset=".05" stop-color="#ffffff" stop-opacity=".5"/>'
    '<stop offset=".12" stop-color="#ffffff" stop-opacity="0"/><stop offset=".88" stop-color="#ffffff" stop-opacity="0"/>'
    '<stop offset=".95" stop-color="#ffffff" stop-opacity=".35"/><stop offset="1" stop-color="#000000" stop-opacity=".24"/></linearGradient>'
    '<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#c4c6cb"/><stop offset="1" stop-color="#8c8e93"/></linearGradient>'
    '<linearGradient id="lip-white" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#e2e4e8"/><stop offset="1" stop-color="#c3c6cc"/></linearGradient>'
    '<linearGradient id="plastic" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e4e6ea"/></linearGradient>'
    '<linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#e9eaed"/><stop offset=".5" stop-color="#a9abb1"/><stop offset="1" stop-color="#d8d9dd"/></linearGradient>'
    '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#2a2d34"/><stop offset="1" stop-color="#0b0c0f"/></linearGradient>'
    '<linearGradient id="wall" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#1d6bff"/><stop offset=".5" stop-color="#7a3cff"/><stop offset="1" stop-color="#ff5a7a"/></linearGradient>'
    '<linearGradient id="label" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#2f80ff"/><stop offset="1" stop-color="#1550d6"/></linearGradient>'
    '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#f1d58a"/><stop offset="1" stop-color="#c39a3c"/></linearGradient>'
    '<radialGradient id="cone" cx=".42" cy=".38" r=".7">'
    '<stop offset="0" stop-color="#4a4d54"/><stop offset="1" stop-color="#121316"/></radialGradient>'
    '<radialGradient id="lens" cx=".4" cy=".35" r=".7">'
    '<stop offset="0" stop-color="#3a5fae"/><stop offset=".6" stop-color="#14203d"/><stop offset="1" stop-color="#05070c"/></radialGradient>'
    '<radialGradient id="disc" cx=".5" cy=".5" r=".5">'
    '<stop offset=".2" stop-color="#f7f8fa"/><stop offset="1" stop-color="#b9bcc3"/></radialGradient>'
    '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset=".2" stop-color="#ff7ad9" stop-opacity="0"/><stop offset=".38" stop-color="#ff7ad9" stop-opacity=".4"/>'
    '<stop offset=".52" stop-color="#5fd3ff" stop-opacity=".4"/><stop offset=".66" stop-color="#9dff7a" stop-opacity=".32"/>'
    '<stop offset=".82" stop-color="#ffe066" stop-opacity="0"/></linearGradient>'
    '<radialGradient id="shadow" cx=".5" cy=".5" r=".5">'
    '<stop offset="0" stop-color="#000000" stop-opacity=".32"/><stop offset="1" stop-color="#000000" stop-opacity="0"/></radialGradient>'
)


def rr(x, y, w, h, r):
    return f'M{x + r} {y}h{w - 2 * r}a{r} {r} 0 0 1 {r} {r}v{h - 2 * r}a{r} {r} 0 0 1-{r} {r}h-{w - 2 * r}a{r} {r} 0 0 1-{r}-{r}v-{h - 2 * r}a{r} {r} 0 0 1 {r}-{r}z'


def shadow(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx * .13:.2f}" fill="url(#shadow)"/>'


def body(x, y, w, h, r, fill="alu"):
    """A slab of material with cylindrical side shading, a top highlight and an outline."""
    d = rr(x, y, w, h, r)
    return (f'<path d="{d}" fill="url(#{fill})"/><path d="{d}" fill="url(#side)"/>'
            f'<path d="M{x + r} {y + .5}h{w - 2 * r}" stroke="#ffffff" stroke-opacity=".8" stroke-width=".8" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" {INK_EDGE}/>')


def lip(x, y, w, h, fill="lip"):
    """The bottom face of an object seen almost straight on."""
    d = rr(x, y, w, h, h / 2)
    return f'<path d="{d}" fill="url(#{fill})"/><path d="{d}" fill="url(#side)"/><path d="{d}" fill="none" {INK_EDGE}/>'


def deboss(d, base="#aeb0b5"):
    """A mark pressed into the surface: a light rim below, the mark slightly darker."""
    return (f'<path d="{d}" fill="#ffffff" fill-opacity=".7" transform="translate(0 .5)"/>'
            f'<path d="{d}" fill="{base}"/>')


def glass(x, y, w, h, r):
    d = rr(x, y, w, h, r)
    return f'<path d="{d}" fill="url(#glass)"/>'


def screen(x, y, w, h, r):
    d = rr(x, y, w, h, r)
    return (f'<path d="{d}" fill="url(#wall)"/>'
            f'<path d="M{x} {y}h{w * .55}L{x} {y + h * .8}z" fill="#ffffff" fill-opacity=".1"/>')


def ring(cx, cy, r_out, r_in):
    return (f'M{cx} {cy - r_out}a{r_out} {r_out} 0 1 1 0 {2 * r_out}a{r_out} {r_out} 0 1 1 0-{2 * r_out}z'
            f'M{cx} {cy - r_in}a{r_in} {r_in} 0 1 0 0 {2 * r_in}a{r_in} {r_in} 0 1 0 0-{2 * r_in}z')


def badge(fig):
    return ('<circle cx="51" cy="13" r="8.5" fill="url(#label)" stroke="#ffffff" stroke-width="1.4"/>'
            f'<g transform="translate(44.6 6.6) scale(.8)"><path fill="none" stroke="#ffffff" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" d="{fig}"/></g>')


def drive(x, y, w, h, fill="alu"):
    return body(x, y, w, h, 6, fill) + lip(x, y + h - 7, w, 7)


def harddisk():
    return shadow(32, 57, 18) + drive(16, 8, 32, 47) + deboss(ring(32, 28, 7, 2.4), "#b4b6bb")


def multidisk():
    return (shadow(32, 57.5, 22) + drive(24, 4, 30, 42, "alu-dark") + drive(10, 12, 30, 44)
            + deboss(ring(25, 31, 6, 2), "#b4b6bb"))


def removable_drive():
    cable = ('<path d="M48 41h4.5a4 4 0 0 1 4 4v5" fill="none" stroke="#8c8e93" stroke-width="3.2" stroke-linecap="round"/>'
             '<path d="M48 41h4.5a4 4 0 0 1 4 4v5" fill="none" stroke="#e4e5e8" stroke-width="2" stroke-linecap="round"/>'
             '<rect x="54" y="49" width="5" height="6.4" rx="1.4" fill="url(#steel)" ' + INK_EDGE + '/>')
    return shadow(30, 55, 22) + cable + drive(8, 18, 42, 33) + deboss(ring(29, 32, 5.5, 1.8), "#b4b6bb")


def optical_drive():
    disc = (f'<path fill-rule="evenodd" d="{ring(32, 26, 18, 2.4)}" fill="url(#disc)"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 26, 18, 2.4)}" fill="url(#sheen)"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 26, 18, 2.4)}" fill="none" {INK_EDGE}/>')
    eject = "M48 38.6l2.6-3 2.6 3zM48 40.2h5.2"
    return (shadow(32, 55, 27) + disc + body(5, 30, 54, 20, 5) + lip(5, 44, 54, 6)
            + deboss(rr(12, 37, 30, 2.4, 1.2), "#3a3c41") + deboss(eject, "#a3a5aa"))


def optical_disc():
    d = ring(32, 29, 24, 2.8)
    return (shadow(32, 57, 18) + f'<path fill-rule="evenodd" d="{d}" fill="url(#disc)"/>'
            f'<path fill-rule="evenodd" d="{d}" fill="url(#sheen)"/>'
            f'<path fill-rule="evenodd" d="{ring(32, 29, 8.5, 2.8)}" fill="#ffffff" fill-opacity=".55"/>'
            f'<path fill-rule="evenodd" d="{d}" fill="none" {INK_EDGE}/>'
            f'<circle cx="32" cy="29" r="8.5" fill="none" stroke="#000000" stroke-opacity=".12" stroke-width=".6"/>')


def usb_stick():
    return (shadow(32, 57, 12) + body(25, 4, 14, 12, 1.6, "steel")
            + '<rect x="27.5" y="7" width="9" height="3.2" rx="1" fill="#2c2e33"/>'
            + drive(21, 14, 22, 41) + '<circle cx="32" cy="46" r="2.2" fill="#2c2e33"/>'
            + '<path d="M30.2 46.8a2.2 2.2 0 0 0 3.6 0" stroke="#ffffff" stroke-opacity=".5" stroke-width=".5" fill="none"/>')


def sd_card():
    d = "M18 7h22l9 9v38a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V10a3 3 0 0 1 3-3z"
    contacts = "".join(f'<rect x="{19 + i * 3.6:.1f}" y="9" width="2.4" height="8" rx=".6" fill="url(#gold)"/>' for i in range(6))
    return (shadow(32, 58, 17) + f'<path d="{d}" fill="url(#plastic)"/><path d="{d}" fill="url(#side)"/>'
            + contacts + '<rect x="19" y="26" width="26" height="24" rx="2.6" fill="url(#label)"/>'
            + '<rect x="19" y="26" width="26" height="7" rx="2.6" fill="#ffffff" fill-opacity=".18"/>'
            + '<rect x="13.4" y="30" width="2.2" height="8" rx=".8" fill="#c9cbd0"/>'
            + f'<path d="{d}" fill="none" {INK_EDGE}/>')


def laptop():
    base = "M3 43.5h58l-2.4 6.4a2.4 2.4 0 0 1-2.2 1.6H7.6a2.4 2.4 0 0 1-2.2-1.6z"
    return (shadow(32, 54, 29) + body(8, 8, 48, 36, 3.4) + glass(9, 9, 46, 34, 2.8) + screen(11, 11, 42, 30, 1)
            + f'<path d="{base}" fill="url(#alu)"/><path d="{base}" fill="url(#side)"/><path d="{base}" fill="none" {INK_EDGE}/>'
            + '<path d="M3.4 44.2h57.2" stroke="#ffffff" stroke-opacity=".9" stroke-width=".8"/>'
            + deboss(rr(27, 43.6, 10, 1.8, .9), "#a7a9ae"))


def display():
    return (shadow(32, 58, 18) + '<path d="M27 42h10l2.6 11h-15.2z" fill="url(#alu-dark)"/>'
            + '<path d="M27 42h10l2.6 11h-15.2z" fill="none" ' + INK_EDGE + '/>'
            + body(18, 52, 28, 4, 2) + body(5, 6, 54, 38, 3) + glass(6, 7, 52, 36, 2.4) + screen(8.4, 9.4, 47.2, 31.2, .8))


def phone():
    return (shadow(32, 59, 13) + body(19, 4, 26, 53, 7.4, "steel") + glass(20.4, 5.4, 23.2, 50.2, 6.2)
            + screen(21.8, 6.8, 20.4, 47.4, 5) + '<rect x="28.2" y="9.2" width="7.6" height="2.6" rx="1.3" fill="#000000"/>')


def ebook():
    lines = "".join(f'<path d="M21.5 {14 + i * 4}h{21 - (8 if i == 6 else 0)}" stroke="#a7a49a" stroke-width="1.1" stroke-linecap="round"/>' for i in range(7))
    return (shadow(32, 58, 15) + body(15, 4, 34, 52, 5, "plastic")
            + '<rect x="18.5" y="8" width="27" height="38" rx="1.2" fill="#ecebe5" stroke="#000000" stroke-opacity=".12" stroke-width=".5"/>'
            + lines)


def drawing_tablet():
    pen = ('<path d="M22 46 48 18" stroke="#8c8e93" stroke-width="4.2" stroke-linecap="round"/>'
           '<path d="M22 46 48 18" stroke="#fbfbfc" stroke-width="3" stroke-linecap="round"/>'
           '<path d="M22 46l2.2-2.4" stroke="#55585e" stroke-width="3" stroke-linecap="round"/>')
    return (shadow(32, 55, 29) + body(3, 14, 58, 36, 5) + lip(3, 44, 58, 6)
            + glass(9, 18, 46, 24, 2) + '<path d="M9 18h25L9 38z" fill="#ffffff" fill-opacity=".06"/>' + pen)


def keyboard():
    keys, y = [], 22.2
    for row, (h, n, wide) in enumerate([(2.6, 14, None), (4, 13, "tail"), (4, 13, "head"), (4, 12, "both"), (4, 9, "space")]):
        x, unit = 5.6, (52.8 - .8 * (n - 1)) / n
        widths = [unit] * n
        if wide == "space":
            widths = [unit] * 3 + [unit * 3 + 1.6] + [unit] * 3
        elif wide == "tail":
            widths[-1] += unit * .5; widths[0] -= unit * .5
        elif wide == "head":
            widths[0] += unit * .5; widths[-1] -= unit * .5
        elif wide == "both":
            widths[0] += unit * .7; widths[-1] += unit * .7
        scale = 52.8 / (sum(widths) + .8 * (len(widths) - 1))
        for w in widths:
            w *= scale
            keys.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h}" rx=".8" fill="url(#plastic)" stroke="#000000" stroke-opacity=".18" stroke-width=".35"/>')
            x += w + .8
        y += h + .8
    return shadow(32, 49.5, 30) + body(3, 20, 58, 25, 3.4) + lip(3, 42, 58, 4.4) + "".join(keys)


def mouse():
    return (shadow(32, 57.5, 13) + body(20, 7.6, 24, 48, 12, "alu-dark") + body(20, 5, 24, 48, 12, "plastic")
            + '<ellipse cx="27" cy="17" rx="3" ry="7" fill="#ffffff" fill-opacity=".8"/>')


def gamepad():
    d = ("M20 16h24c6.5 0 9.6 3.6 11.4 9.4l3.6 12.4c1.5 5.2-3.2 9.3-7.8 6.6L45 40H19l-6.2 4.4"
         "c-4.6 2.7-9.3-1.4-7.8-6.6l3.6-12.4C10.4 19.6 13.5 16 20 16z")
    buttons = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#c4c7cd"/>' for x, y in ((45, 22), (49, 26), (45, 30), (41, 26)))
    sticks = "".join(f'<circle cx="{x}" cy="34" r="3.8" fill="url(#cone)" stroke="#000000" stroke-opacity=".3" stroke-width=".5"/>'
                     f'<circle cx="{x}" cy="34" r="2.4" fill="none" stroke="#ffffff" stroke-opacity=".18" stroke-width=".6"/>' for x in (25, 39))
    return (shadow(32, 51, 26) + f'<path d="{d}" fill="url(#plastic)"/><path d="{d}" fill="url(#side)"/>'
            + deboss("M17.6 21.4h3.2v3.2h3.2v3.2h-3.2v3.2h-3.2v-3.2h-3.2v-3.2h3.2z", "#c4c7cd") + buttons + sticks
            + f'<path d="{d}" fill="none" {INK_EDGE}/>')


def headphones(mic=False):
    band = ('<path d="M14.6 30V25a17.4 17.4 0 0 1 34.8 0v5" fill="none" stroke="#8c8e93" stroke-width="4.6" stroke-linecap="round"/>'
            '<path d="M14.6 30V25a17.4 17.4 0 0 1 34.8 0v5" fill="none" stroke="url(#steel)" stroke-width="3.4" stroke-linecap="round"/>'
            '<path d="M17.4 28V25.4a14.6 14.6 0 0 1 29.2 0V28" fill="none" stroke="#f4f5f7" stroke-width="2" stroke-linecap="round"/>')
    cups = (body(6, 28, 15, 25, 6.5) + '<rect x="17" y="30.5" width="6" height="20" rx="3" fill="url(#plastic)" ' + INK_EDGE + '/>'
            + body(43, 28, 15, 25, 6.5) + '<rect x="41" y="30.5" width="6" height="20" rx="3" fill="url(#plastic)" ' + INK_EDGE + '/>')
    boom = ('<path d="M12 52c1 4.4 6 5.4 13 5.4" fill="none" stroke="#8c8e93" stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M12 52c1 4.4 6 5.4 13 5.4" fill="none" stroke="#e4e5e8" stroke-width="1.4" stroke-linecap="round"/>'
            '<rect x="23.6" y="55.4" width="6.6" height="4" rx="2" fill="url(#cone)"/>') if mic else ""
    return shadow(32, 58, 24) + band + cups + boom


def speaker():
    return (shadow(32, 58, 17) + drive(14, 6, 36, 51)
            + f'<path fill-rule="evenodd" d="{ring(32, 34, 12.5, 11)}" fill="#ffffff" fill-opacity=".6"/>'
            + '<circle cx="32" cy="34" r="11" fill="url(#cone)"/><circle cx="32" cy="34" r="3.6" fill="#2b2d32" stroke="#ffffff" stroke-opacity=".12" stroke-width=".6"/>'
            + '<circle cx="32" cy="15" r="4.4" fill="url(#cone)" stroke="#ffffff" stroke-opacity=".6" stroke-width=".8"/>')


def webcam():
    clip = "M26 36h12v4h7a2 2 0 0 1 2 2v3H17v-3a2 2 0 0 1 2-2h7z"
    return (shadow(32, 48, 16) + f'<path d="{clip}" fill="url(#alu-dark)"/><path d="{clip}" fill="none" {INK_EDGE}/>'
            + body(12, 17, 40, 20, 10) + '<circle cx="32" cy="27" r="8.2" fill="url(#steel)" ' + INK_EDGE + '/>'
            + '<circle cx="32" cy="27" r="6.8" fill="#0b0c0f"/><circle cx="32" cy="27" r="4" fill="url(#lens)"/>'
            + '<circle cx="30.6" cy="25.6" r="1.1" fill="#ffffff" fill-opacity=".7"/><circle cx="44.6" cy="27" r=".9" fill="#30d158"/>')


def microphone():
    grille = "".join(f'<path d="M23 {8 + i * 2.2}h18" stroke="#ffffff" stroke-opacity=".35" stroke-width=".5"/>' for i in range(10))
    yoke = ('<path d="M18.5 20v5a13.5 13.5 0 0 0 27 0v-5" fill="none" stroke="#8c8e93" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M18.5 20v5a13.5 13.5 0 0 0 27 0v-5" fill="none" stroke="url(#steel)" stroke-width="2" stroke-linecap="round"/>')
    return (shadow(32, 58, 15) + body(30.6, 38, 2.8, 14, 1.2, "steel") + yoke + body(22, 4, 20, 30, 10, "alu-dark")
            + grille + body(22, 22, 20, 3.2, 1.6, "steel") + body(19, 50, 26, 5, 2.5) )


def printer():
    paper = "M15 33.6h34l1.8 13.4H13.2z"
    return (shadow(32, 55, 28) + '<rect x="17" y="4" width="30" height="16" fill="url(#plastic)" ' + INK_EDGE + '/>'
            + body(5, 15, 54, 34, 5, "plastic") + lip(5, 43, 54, 6, "lip-white")
            + deboss(rr(13, 31, 38, 2.6, 1.3), "#2c2e33") + glass(43, 20, 10, 4.6, 1.2)
            + '<circle cx="11" cy="22.4" r="1" fill="#30d158"/>'
            + f'<path d="{paper}" fill="url(#plastic)"/><path d="{paper}" fill="none" {INK_EDGE}/>'
            + '<path d="M18 38h20M17.6 41.4h26" stroke="#b9bcc3" stroke-width=".9" stroke-linecap="round"/>')


def scanner():
    lid = "M10 18h44a3 3 0 0 1 2.8 1.9L60 28H4l3.2-8.1A3 3 0 0 1 10 18z"
    return (shadow(32, 53, 29) + f'<path d="{lid}" fill="url(#plastic)"/><path d="{lid}" fill="none" {INK_EDGE}/>'
            + '<path d="M10.4 19h43.2" stroke="#ffffff" stroke-width=".8" stroke-linecap="round"/>'
            + deboss(rr(16, 22, 32, 2.2, 1.1), "#d3d6db")
            + body(4, 28, 56, 20, 3.6, "plastic") + lip(4, 43, 56, 5, "lip-white")
            + '<rect x="7" y="28.6" width="50" height="1.6" rx=".8" fill="#7fe3ff"/>'
            + '<rect x="7" y="28.6" width="50" height="1.6" rx=".8" fill="#ffffff" fill-opacity=".45"/>'
            + '<circle cx="53" cy="37" r="1.5" fill="#c4c7cd"/><circle cx="48.6" cy="37" r=".9" fill="#30d158"/>')


def network_printer(wifi):
    return printer() + badge(wifi)


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
    out["printer-network"] = network_printer(glyph("network-wireless"))
    return {name: ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 64 64">'
                   f"<defs>{DEFS}</defs>{body_}</svg>\n") for name, body_ in sorted(out.items())}
