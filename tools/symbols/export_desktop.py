#!/usr/bin/env python3
"""Write the theme's symbols into the code of the Malaysia desktop, so the desktop draws what
GTK and Qt apps show.

Usage: python3 tools/symbols/export_desktop.py <malaysia-path> <barrierkit-path>

For every Symbol and menu bar icon, the drawing of its name in Malaysia/symbolic (MacTahoe's,
or Malaysia's own source) becomes filled outlines on the 16 px grid:
  barrierkit/crates/bk/src/symbol.rs                      the path of each Symbol (opaque parts)
  malaysia/crates/malaysia-shell/src/menubar/icons.rs     each icon, with its translucent parts
  malaysia/crates/malaysia-services/src/networkmanager.rs the three bands of the Wi-Fi signal

Also writes docs/symbols.md with the Symbol/constant → theme name table.
"""
import glob, os, re, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export import convert
from picosvg.svg import SVG
from picosvg.svg_types import SVGPath

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIGNAL = "network-wireless-signal-excellent"


# key → name in the theme, or (name, context) when the name is new.
# A freedesktop/Adwaita name when the meaning matches; otherwise the name of the drawn object
# (like phone-symbolic or tv-symbolic), so an existing name never changes meaning.
BK = {
    "MagnifyingGlass": "system-search", "XMark": "window-close", "SpeakerWave": "audio-volume-high",
    "Plus": "list-add", "Minus": "list-remove", "Ellipsis": "view-more-horizontal",
    "ChevronUpDown": ("pan-up-down", "actions"), "ChevronRight": "go-next", "ChevronLeft": "go-previous",
    "ChevronUp": "go-up", "ChevronDown": "go-down", "CircleHalf": ("dark-mode", "status"),
    "Play": "media-playback-start", "Pause": "media-playback-pause", "Shuffle": "media-playlist-shuffle",
    "ChevronLeftForwardSlashChevronRight": ("text-x-script", "mimetypes"),
    "Backward": "media-skip-backward", "Forward": "media-skip-forward", "ListBullet": "view-list-bullet",
    "SquareGrid": "view-grid", "SlidersVertical": "preferences-other", "SidebarLeft": "sidebar-show",
    "House": "go-home", "Tv": "tv", "Film": "video-x-generic", "Star": "non-starred", "StarFill": "starred",
    "Clock": "document-open-recent", "Bookmark": "user-bookmarks", "ArrowDown": ("arrow-down", "actions"),
    "Checkmark": "object-select", "Captions": "media-view-subtitles", "Expand": "view-fullscreen",
    "GoBackward": "edit-undo", "GoForward": "edit-redo", "Folder": "folder", "Document": "text-x-generic",
    "ChevronDoubleRight": "go-last", "Accessibility": "preferences-desktop-accessibility",
    "Display": "video-display", "MenubarDockRectangle": ("preferences-desktop-dock", "categories"),
    "Photo": ("photo", "actions"), "Moon": "weather-clear-night", "Bell": "preferences-system-notifications",
    "Bed": ("bed", "status"), "Person": "avatar-default", "Briefcase": ("briefcase", "status"),
    "Printer": "printer", "Phone": "phone", "SquareOnSquare": "edit-copy", "Wifi": "network-wireless",
    "Bluetooth": "bluetooth", "Network": "network-workgroup", "Lock": "system-lock-screen",
    "Bolt": ("bolt", "status"), "Battery": "battery", "Keyboard": "input-keyboard",
    "QuestionMark": "dialog-question", "EllipsisCircle": "view-more", "Square": ("square", "actions"),
    "Circle": ("circle", "actions"),
}
SHELL = {
    "HALF_LEFT": "window-tile-left", "HALF_RIGHT": "window-tile-right", "HALF_TOP": "window-tile-top",
    "HALF_BOTTOM": "window-tile-bottom", "QUARTER_TOP_LEFT": "window-tile-top-left",
    "QUARTER_TOP_RIGHT": "window-tile-top-right", "QUARTER_BOTTOM_LEFT": "window-tile-bottom-left",
    "QUARTER_BOTTOM_RIGHT": "window-tile-bottom-right", "HALVES_LEFT_RIGHT": "window-tile-left-right",
    "HALVES_RIGHT_LEFT": "window-tile-right-left", "HALVES_TOP_BOTTOM": "window-tile-top-bottom",
    "HALVES_BOTTOM_TOP": "window-tile-bottom-top", "GRID": "window-tile-grid",
    "INFO": "help-about", "HELP": "help-browser", "GEAR": "emblem-system", "TRASH": "user-trash",
    "HOUSE": "user-home", "DESKTOP": "user-desktop", "DOCUMENTS": "folder-documents",
    "DOWNLOADS": "folder-download", "PICTURES": "folder-pictures", "MUSIC": "folder-music",
    "VIDEOS": "folder-videos", "SHARE": "send-to", "EJECT": "media-eject", "EMOJI": ("face-smile", "actions"),
    "VIEW_LIST": "view-list", "VIEW_COLUMNS": ("view-column", "actions"), "VIEW_GALLERY": "view-paged",
    "APPS": "view-app-grid", "BOOK": ("help-contents", "actions"), "LAPTOP": "computer",
    "FILE": ("application-x-generic", "mimetypes"), "FILE_TEXT": "x-office-document",
    "FILE_IMAGE": "image-x-generic",
}
# icons.rs constants drawn like a Symbol, and code that keeps its own drawing, and why.
SAME = {"SEARCH": "MagnifyingGlass", "PRINTER": "Printer", "KEYBOARD": "Keyboard"}
SKIP = {
    "MENU_ITEM": "two-color template ({{text}} and {{accent}}) that the menu fills in at runtime",
    "CapsuleOnRectangle": "a picture of a Settings choice (window controls shape), not an icon apps ask for",
    "CapsuleOnRectangleFill": "a picture of a Settings choice (window controls shape), not an icon apps ask for",
}


def name(entry):
    return entry if isinstance(entry, str) else entry[0]


def drawing(theme_name):
    """(file in Malaysia/symbolic, [(opacity, d)]) for a theme name."""
    path = glob.glob(f"{ROOT}/Malaysia/symbolic/*/{theme_name}-symbolic.svg")[0]
    return path, flat(open(os.path.realpath(path), encoding="utf-8").read())


def flat(text):
    """Filled outlines by opacity, with transforms and strokes applied (picosvg)."""
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    tag = text.index("<svg")
    if not re.search(r"\bxmlns\s*=", text[tag:text.index(">", tag)]):
        text = text.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write(SVG.fromstring(text).topicosvg().tostring())
    try:
        return layers(convert(f.name))
    finally:
        os.remove(f.name)


def layers(svg):
    return [(float(a or 1), d) for a, d in re.findall(r'<path fill="[^"]+"(?: opacity="([^"]+)")? d="([^"]+)"/>', svg)]


def outline(d, fill):
    """Filled outline of a stroked Symbol path, as barrierkit drew it before."""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
                f'<path d="{d}" fill="{fill}" stroke="#000" stroke-width="1.4" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')
    try:
        return layers(convert(f.name))
    finally:
        os.remove(f.name)


def opaque(parts):
    return "".join(d for a, d in parts if a == 1)


def arm(key, d):
    line = f'            Self::{key} => "{d}",\n'
    return line if len(line) <= 101 else f'            Self::{key} => {{\n                "{d}"\n            }}\n'


def write_symbols(path):
    src = open(path, encoding="utf-8").read()
    start = src.index("        match self {\n", src.index("fn path(self)")) + len("        match self {\n")
    end = src.index("        }\n    }\n}\n", start)
    old = dict(re.findall(r'Self::(\w+) => \{?\s*"([^"]+)"', src[start:end]))
    variants = re.findall(r"^    (\w+),$", src[src.index("pub enum Symbol {"):src.index("impl Symbol")], re.M)
    rows, arms = [], ""
    for key in variants:
        if key in SKIP:
            parts = outline(old[key], "currentColor" if key.endswith("Fill") else "none")
            rows.append(("barrierkit `Symbol`", f"Symbol::{key}", "—", "—", SKIP[key]))
        else:
            file, parts = drawing(name(BK[key]))
            rows.append(("barrierkit `Symbol`", f"Symbol::{key}", f"{name(BK[key])}-symbolic", origin(file), "drawn from the theme"))
        arms += arm(key, opaque(parts))
    open(path, "w", encoding="utf-8").write(src[:start] + arms + src[end:])
    return rows


def origin(file):
    return "MacTahoe" if not os.path.exists(file.replace("/Malaysia/symbolic/", "/src/malaysia-symbolic/")) else "Malaysia"


def svg(parts):
    body = "".join('<path fill=\\"currentColor\\"' + (f' opacity=\\"{a:g}\\"' if a < 1 else "") + f' d=\\"{d}\\"/>'
                   for a, d in parts)
    return ('<svg xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"16\\" height=\\"16\\" viewBox=\\"0 0 16 16\\">'
            + body + "</svg>")


def write_shell(path):
    src = open(path, encoding="utf-8").read()
    rows = []

    def swap(m):
        key = m.group(1)
        if key in SKIP:
            rows.append(("malaysia-shell `icons.rs`", f"icons::{key}", "—", "—", SKIP[key]))
            return m.group(0)
        theme_name = name(BK[SAME[key]]) if key in SAME else name(SHELL[key])
        file, parts = drawing(theme_name)
        rows.append(("malaysia-shell `icons.rs`", f"icons::{key}", f"{theme_name}-symbolic", origin(file), "drawn from the theme"))
        return f'pub(crate) const {key}: &str = "{svg(parts)}";'
    src = re.sub(r'pub\(crate\) const (\w+): &str = "(.*)";', swap, src)
    open(path, "w", encoding="utf-8").write(src)
    return rows


def write_signal(path):
    """The bands of the Wi-Fi signal from the inside out, as the menu bar lights them."""
    file = os.path.realpath(glob.glob(f"{ROOT}/Malaysia/symbolic/*/{SIGNAL}-symbolic.svg")[0])
    bands = []
    for d in re.findall(r' d="([^"]+)"', open(file, encoding="utf-8").read()):
        bands.append(opaque(flat(f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="{d}"/></svg>')))
    bands.sort(key=lambda d: -SVGPath(d=d).bounding_box().y)
    src = open(path, encoding="utf-8").read()
    body = "".join(f'    "{d}",\n' for d in bands)
    src = re.sub(r'const ARCS: \[&str; 3\] = \[\n.*?\];', lambda _: f"const ARCS: [&str; 3] = [\n{body}];", src, flags=re.S)
    open(path, "w", encoding="utf-8").write(src)


def main(mal, bk):
    rows = write_symbols(f"{bk}/crates/bk/src/symbol.rs")
    rows += write_shell(f"{mal}/crates/malaysia-shell/src/menubar/icons.rs")
    write_signal(f"{mal}/crates/malaysia-services/src/networkmanager.rs")
    with open(f"{ROOT}/docs/symbols.md", "w", encoding="utf-8") as f:
        f.write("# Desktop symbols in the theme\n\n"
                "Generated by `tools/symbols/export_desktop.py`; do not edit. The desktop draws every symbol "
                "below with the theme's drawing of its name, so GTK and Qt apps and the desktop look the same.\n\n"
                "| Source | Code | Name in the theme | Drawing | Status |\n|---|---|---|---|---|\n")
        for r in rows:
            f.write("| " + " | ".join(f"`{c}`" if i in (1, 2) and c != "—" else c for i, c in enumerate(r)) + " |\n")
    print(f"{len(rows)} desktop symbols drawn from the theme")


if __name__ == "__main__":
    main(*sys.argv[1:3])
