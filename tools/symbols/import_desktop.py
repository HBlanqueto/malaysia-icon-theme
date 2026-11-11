#!/usr/bin/env python3
"""Import the symbols the Malaysia desktop draws in code and save them as editable stroke
sources in src/malaysia-symbolic/<context>/<name>.svg.

Usage: python3 tools/symbols/import_desktop.py <malaysia-path> <barrierkit-path>

Sources:
  barrierkit/crates/bk/src/symbol.rs                    Symbol enum (16 px grid, components.symbol.stroke)
  malaysia/crates/malaysia-shell/src/menubar/icons.rs   menu bar icons

Also writes docs/symbols.md with the Symbol/constant → theme name table.
Run tools/symbols/export.py afterwards.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "src", "malaysia-symbolic")
INK = "#2e3436"

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
# icons.rs constants that are not imported, and why.
SKIP = {
    "SEARCH": "same name as Symbol::MagnifyingGlass (system-search); barrierkit's drawing wins",
    "PRINTER": "same name as Symbol::Printer (printer); barrierkit's drawing wins",
    "KEYBOARD": "same name as Symbol::Keyboard (input-keyboard); barrierkit's drawing wins",
    "MENU_ITEM": "two-color template ({{text}} and {{accent}}) that the menu fills in at runtime",
}

# Last Adwaita commit before the fork; tells whether a name already existed in Adwaita 51.0.
ADWAITA_BASE = "75a7cc2"

# current context of every name in the theme
existing = {}
for ctx in os.listdir(f"{ROOT}/Malaysia/symbolic"):
    for f in os.listdir(f"{ROOT}/Malaysia/symbolic/{ctx}"):
        existing[f.removesuffix(".svg")] = ctx
upstream = {os.path.basename(p).removesuffix(".svg") for p in subprocess.run(
    ["git", "-C", ROOT, "ls-tree", "-r", "--name-only", ADWAITA_BASE, "Adwaita/symbolic"],
    capture_output=True, text=True, check=True).stdout.split()}


def target(entry):
    name, ctx = (entry, None) if isinstance(entry, str) else entry
    full = f"{name}-symbolic"
    return full, existing.get(full) or ctx or "actions", full in upstream


def bk_symbols(path):
    src = open(path, encoding="utf-8").read()
    body = src[src.index("fn path(self)"):]
    for m in re.finditer(r"Self::(\w+)(?:\s*\|\s*Self::(\w+))?\s*=>\s*\{?\s*\"([^\"]+)\"", body):
        k1, k2, d = m.groups()
        for k in filter(None, (k1, k2)):
            fill = INK if k.endswith("Fill") else "none"
            yield k, (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
                      f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="1.4" '
                      f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def shell_icons(path):
    for m in re.finditer(r'pub const (\w+): &str = "(.*)";', open(path, encoding="utf-8").read()):
        svg = m.group(2).encode().decode("unicode_escape").replace("currentColor", INK)
        yield m.group(1), svg


def main(mal, bk):
    stroke = json.load(open(f"{bk}/crates/ctdesign/tengen/components.json"))["components"]["symbol"]["stroke"]
    rows, seen = [], {}
    sources = [("barrierkit `Symbol`", "Symbol::", BK, bk_symbols(f"{bk}/crates/bk/src/symbol.rs")),
               ("malaysia-shell `icons.rs`", "icons::", SHELL, shell_icons(f"{mal}/crates/malaysia-shell/src/menubar/icons.rs"))]
    for label, prefix, table, items in sources:
        for key, svg in items:
            if key in SKIP:
                rows.append((label, prefix + key, "—", "—", SKIP[key]))
                continue
            if key not in table:
                sys.exit(f"{prefix}{key} no tiene nombre asignado en import_desktop.py")
            name, ctx, replaces = target(table[key])
            if name in seen:
                sys.exit(f"{name} asignado dos veces: {seen[name]} y {prefix}{key}")
            seen[name] = prefix + key
            if prefix == "Symbol::":
                svg = svg.replace('stroke-width="1.4"', f'stroke-width="{stroke}"')
            os.makedirs(f"{SRC}/{ctx}", exist_ok=True)
            open(f"{SRC}/{ctx}/{name}.svg", "w", encoding="utf-8").write(svg + "\n")
            rows.append((label, prefix + key, name, ctx, "replaces Adwaita's" if replaces else "new"))
    with open(f"{ROOT}/docs/symbols.md", "w", encoding="utf-8") as f:
        f.write("# Desktop symbols in the theme\n\n"
                "Generated by `tools/symbols/import_desktop.py`; do not edit. Every symbol the desktop draws in code "
                "has its file in `Malaysia/symbolic/<context>/<name>.svg`; the editable stroke source is in "
                "`src/malaysia-symbolic/`.\n\n"
                "| Source | Code | Name in the theme | Context | Status |\n|---|---|---|---|---|\n")
        for r in rows:
            f.write("| " + " | ".join(f"`{c}`" if i in (1, 2) and c != "—" else c for i, c in enumerate(r)) + " |\n")
        f.write("\n## For barrierkit\n\n"
                "Name `Symbol` should ask the icon theme for. If the theme does not have it, "
                "`Symbol::path()` keeps drawing the stroke.\n\n```rust\n"
                "impl Symbol {\n    pub fn icon_name(self) -> &'static str {\n        match self {\n")
        for r in rows:
            if r[1].startswith("Symbol::"):
                f.write(f'            Self::{r[1].removeprefix("Symbol::")} => "{r[2]}",\n')
        f.write("        }\n    }\n}\n```\n")
    new = sum(1 for r in rows if r[4] == "new")
    print(f"{len(seen)} fuentes en src/malaysia-symbolic ({new} nuevas, {len(seen) - new} reemplazan a Adwaita); "
          f"{len(SKIP)} omitidas")


if __name__ == "__main__":
    main(*sys.argv[1:3])
