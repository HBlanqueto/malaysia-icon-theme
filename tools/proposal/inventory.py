#!/usr/bin/env python3
"""Inventario de íconos que usa el escritorio Malaysia (repos malaysia + barrierkit)
y su cruce con el pack Adwaita de este repositorio.

Uso: python3 tools/proposal/inventory.py <ruta-malaysia> <ruta-barrierkit>  > inventory.json
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAL, BK = sys.argv[1], sys.argv[2]

theme = {}
for size in ("symbolic", "scalable", "16x16"):
    for ctx in os.listdir(f"{ROOT}/Adwaita/{size}"):
        for f in os.listdir(f"{ROOT}/Adwaita/{size}/{ctx}"):
            theme.setdefault(os.path.splitext(f)[0], []).append(f"{size}/{ctx}")

# Nombre freedesktop/Adwaita candidato por ícono del escritorio (en orden de preferencia)
MAP = {
 # barrierkit Symbol
 "MagnifyingGlass": ["system-search-symbolic", "edit-find-symbolic"], "XMark": ["window-close-symbolic"],
 "SpeakerWave": ["audio-volume-high-symbolic"], "Plus": ["list-add-symbolic"], "Minus": ["list-remove-symbolic"],
 "Ellipsis": ["view-more-horizontal-symbolic", "view-more-symbolic"], "ChevronUpDown": ["pan-up-down-symbolic", "view-sort-ascending-symbolic"],
 "ChevronRight": ["go-next-symbolic", "pan-end-symbolic"], "ChevronLeft": ["go-previous-symbolic", "pan-start-symbolic"],
 "ChevronUp": ["go-up-symbolic", "pan-up-symbolic"], "ChevronDown": ["go-down-symbolic", "pan-down-symbolic"],
 "CircleHalf": ["dark-mode-symbolic", "display-brightness-symbolic"], "Play": ["media-playback-start-symbolic"],
 "Pause": ["media-playback-pause-symbolic"], "Shuffle": ["media-playlist-shuffle-symbolic"],
 "ChevronLeftForwardSlashChevronRight": ["text-x-script-symbolic", "code-symbolic"],
 "Backward": ["media-skip-backward-symbolic"], "Forward": ["media-skip-forward-symbolic"],
 "ListBullet": ["view-list-bullet-symbolic", "view-list-symbolic"], "SquareGrid": ["view-grid-symbolic", "view-app-grid-symbolic"],
 "SlidersVertical": ["preferences-other-symbolic", "emblem-system-symbolic"], "SidebarLeft": ["sidebar-show-symbolic"],
 "House": ["user-home-symbolic", "go-home-symbolic"], "Tv": ["tv-symbolic", "video-display-symbolic"],
 "Film": ["video-x-generic-symbolic"], "Star": ["non-starred-symbolic"], "StarFill": ["starred-symbolic"],
 "Clock": ["document-open-recent-symbolic", "preferences-system-time-symbolic"], "Bookmark": ["user-bookmarks-symbolic", "bookmark-new-symbolic"],
 "ArrowDown": ["folder-download-symbolic", "go-down-symbolic"], "Checkmark": ["object-select-symbolic"],
 "Captions": ["media-view-subtitles-symbolic"], "Expand": ["view-fullscreen-symbolic"],
 "GoBackward": ["edit-undo-symbolic", "object-rotate-left-symbolic"], "GoForward": ["edit-redo-symbolic", "object-rotate-right-symbolic"],
 "Folder": ["folder-symbolic"], "Document": ["text-x-generic-symbolic", "x-office-document-symbolic"],
 "ChevronDoubleRight": ["go-last-symbolic", "media-seek-forward-symbolic"],
 "Accessibility": ["preferences-desktop-accessibility-symbolic"], "Display": ["video-display-symbolic"],
 "MenubarDockRectangle": ["preferences-desktop-appearance-symbolic", "focus-windows-symbolic"],
 "Photo": ["image-x-generic-symbolic"], "Moon": ["weather-clear-night-symbolic", "night-light-symbolic"],
 "Bell": ["preferences-system-notifications-symbolic", "notifications-symbolic"], "Bed": ["system-suspend-symbolic"],
 "Person": ["avatar-default-symbolic", "system-users-symbolic"], "Briefcase": ["applications-office-symbolic"],
 "Printer": ["printer-symbolic"], "Phone": ["phone-symbolic", "call-start-symbolic"], "SquareOnSquare": ["edit-copy-symbolic"],
 "Wifi": ["network-wireless-symbolic", "network-wireless-signal-excellent-symbolic"], "Bluetooth": ["bluetooth-symbolic", "bluetooth-active-symbolic"],
 "Network": ["network-workgroup-symbolic", "web-browser-symbolic", "applications-internet-symbolic"],
 "Lock": ["system-lock-screen-symbolic", "changes-prevent-symbolic"], "Bolt": ["battery-full-charging-symbolic", "thunderbolt-symbolic"],
 "Battery": ["battery-symbolic", "battery-full-symbolic"], "Keyboard": ["input-keyboard-symbolic"],
 "QuestionMark": ["dialog-question-symbolic", "help-browser-symbolic"], "EllipsisCircle": ["view-more-symbolic", "open-menu-symbolic"],
 "Square": ["media-playback-stop-symbolic"], "Circle": ["media-record-symbolic"],
 # malaysia-shell icons.rs
 "HALF_LEFT": ["window-tile-left-symbolic"], "HALF_RIGHT": ["window-tile-right-symbolic"], "HALF_TOP": ["window-tile-top-symbolic"],
 "HALF_BOTTOM": ["window-tile-bottom-symbolic"], "QUARTER_TOP_LEFT": ["window-tile-top-left-symbolic"],
 "QUARTER_TOP_RIGHT": ["window-tile-top-right-symbolic"], "QUARTER_BOTTOM_LEFT": ["window-tile-bottom-left-symbolic"],
 "QUARTER_BOTTOM_RIGHT": ["window-tile-bottom-right-symbolic"], "HALVES_LEFT_RIGHT": ["window-tile-left-right-symbolic"],
 "HALVES_RIGHT_LEFT": ["window-tile-right-left-symbolic"], "HALVES_TOP_BOTTOM": ["window-tile-top-bottom-symbolic"],
 "HALVES_BOTTOM_TOP": ["window-tile-bottom-top-symbolic"], "GRID": ["view-app-grid-symbolic", "view-grid-symbolic"],
 "INFO": ["help-about-symbolic", "dialog-information-symbolic"], "HELP": ["help-browser-symbolic"],
 "MENU_ITEM": ["open-menu-symbolic"], "GEAR": ["emblem-system-symbolic", "preferences-system-symbolic"],
 "SEARCH": ["system-search-symbolic"], "TRASH": ["user-trash-symbolic"], "HOUSE": ["user-home-symbolic"],
 "DESKTOP": ["user-desktop-symbolic"], "DOCUMENTS": ["folder-documents-symbolic"], "DOWNLOADS": ["folder-download-symbolic"],
 "PICTURES": ["folder-pictures-symbolic"], "MUSIC": ["folder-music-symbolic"], "VIDEOS": ["folder-videos-symbolic"],
 "SHARE": ["send-to-symbolic", "emblem-shared-symbolic", "folder-publicshare-symbolic"], "EJECT": ["media-eject-symbolic"],
 "PRINTER": ["printer-symbolic"], "EMOJI": ["face-smile-symbolic", "emoji-people-symbolic"],
 "VIEW_LIST": ["view-list-symbolic"], "VIEW_COLUMNS": ["view-column-symbolic", "view-dual-symbolic"],
 "VIEW_GALLERY": ["view-paged-symbolic", "view-grid-symbolic"], "APPS": ["view-app-grid-symbolic", "applications-system-symbolic"],
 "BOOK": ["accessories-dictionary-symbolic", "help-contents-symbolic"], "KEYBOARD": ["input-keyboard-symbolic"],
 "LAPTOP": ["computer-symbolic", "laptop-symbolic"], "FILE": ["application-x-generic-symbolic", "text-x-generic-symbolic"],
 "FILE_TEXT": ["x-office-document-symbolic", "text-x-generic-symbolic"], "FILE_IMAGE": ["image-x-generic-symbolic"],
 # diálogos y barra
 "POWER_SVG": ["system-shutdown-symbolic"], "RESTART_SVG": ["system-reboot-symbolic"], "LOGOUT_SVG": ["system-log-out-symbolic"],
 "power.svg": ["system-shutdown-symbolic"], "snowflake.svg": ["weather-snow-symbolic", "temperature-symbolic"],
 "wifi (niveles)": ["network-wireless-signal-good-symbolic"], "battery (niveles)": ["battery-level-50-symbolic"],
 # dibujos de dispositivo (Ajustes › Bluetooth)
 "computer.svg": ["computer"], "keyboard.svg": ["input-keyboard"], "mouse.svg": ["input-mouse"], "tablet.svg": ["input-tablet"],
 "gamepad.svg": ["input-gaming"], "headphones.svg": ["audio-headphones"], "speaker.svg": ["audio-speakers", "audio-card"],
 "phone.svg": ["phone"], "generic.svg": ["bluetooth", "preferences-system"],
 "io.github.hblanqueto.malaysia.settings.svg": ["preferences-system", "org.gnome.Settings"],
 "io.github.hblanqueto.malaysia.screenshot.svg": ["applets-screenshooter", "org.gnome.Screenshot"],
}

def status(key):
    cands = MAP.get(key, [])
    for i, c in enumerate(cands):
        if c in theme:
            return ("exact" if i == 0 else "alias"), c, theme[c][0]
    return "missing", (cands[0] if cands else ""), ""

items = []
def add(group, key, svg, where):
    st, name, loc = status(key)
    items.append({"g": group, "k": key, "svg": svg, "src": where, "st": st, "name": name, "loc": loc,
                  "cands": MAP.get(key, [])})

# 1. barrierkit Symbol (trazos en rejilla de 16, stroke 1.4)
src = open(f"{BK}/crates/bk/src/symbol.rs").read()
body = src[src.index("fn path(self)"):]
for m in re.finditer(r"Self::(\w+)(?:\s*\|\s*Self::(\w+))?\s*=>\s*\{?\s*\"([^\"]+)\"", body):
    k1, k2, d = m.groups()
    for k in filter(None, (k1, k2)):
        fill = "currentColor" if k.endswith("Fill") else "none"
        svg = f'<svg viewBox="0 0 16 16"><path d="{d}" fill="{fill}" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        add("barrierkit · Symbol", k, svg, "barrierkit/crates/bk/src/symbol.rs")
# 2. shell icons.rs
for m in re.finditer(r'pub const (\w+): &str = "(.*)";', open(f"{MAL}/crates/malaysia-shell/src/menubar/icons.rs").read()):
    add("malaysia-shell · menú", m.group(1), m.group(2).encode().decode("unicode_escape"), "crates/malaysia-shell/src/menubar/icons.rs")
# 3. diálogos
for m in re.finditer(r'const (\w+_SVG): &str = "(.*)";', open(f"{MAL}/crates/malaysia-shell/src/dialogs.rs").read()):
    add("malaysia-shell · diálogos", m.group(1), m.group(2).encode().decode("unicode_escape"), "crates/malaysia-shell/src/dialogs.rs")
for f in ("power.svg", "snowflake.svg"):
    add("malaysia-shell · barra", f, open(f"{MAL}/crates/malaysia-shell/src/menubar/{f}").read(), f"crates/malaysia-shell/src/menubar/{f}")
wifi = '<svg viewBox="0 0 16 16"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M2 6.5a9 9 0 0 1 12 0"/><path d="M4.3 9a5.5 5.5 0 0 1 7.4 0"/><path d="M6.5 11.4a2.2 2.2 0 0 1 3 0" /></g></svg>'
bat = '<svg viewBox="0 0 24 12"><rect x="0.5" y="0.5" width="20" height="11" rx="3" fill="none" stroke="currentColor" stroke-opacity="0.55"/><rect x="2" y="2" width="9" height="8" rx="1.6" fill="currentColor"/><path d="M22.5 4.5v3" stroke="currentColor" stroke-opacity="0.55" stroke-linecap="round"/></svg>'
add("malaysia-shell · barra", "wifi (niveles)", wifi, "crates/malaysia-services/src/networkmanager.rs (generado)")
add("malaysia-shell · barra", "battery (niveles)", bat, "crates/malaysia-shell/src/menubar/extras.rs (generado)")
# 4. dispositivos y apps
for f in sorted(os.listdir(f"{MAL}/crates/malaysia-settings/assets/devices")):
    add("Ajustes · dispositivos", f, open(f"{MAL}/crates/malaysia-settings/assets/devices/{f}").read(), f"crates/malaysia-settings/assets/devices/{f}")
for f in sorted(os.listdir(f"{MAL}/share/icons/hicolor/scalable/apps")):
    add("Íconos de app", f, open(f"{MAL}/share/icons/hicolor/scalable/apps/{f}").read(), f"share/icons/hicolor/scalable/apps/{f}")

# prefijar ids para que no choquen al incrustarlos
for i, it in enumerate(items):
    s = re.sub(r"<\?xml[^>]*\?>", "", it["svg"])
    for idv in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{idv}"', f'id="m{i}{idv}"').replace(f"#{idv})", f"#m{i}{idv})").replace(f'"#{idv}"', f'"#m{i}{idv}"')
    it["svg"] = s

out = {"items": items, "theme_size": len(theme)}
json.dump(out, sys.stdout, ensure_ascii=False)
from collections import Counter
print(Counter(i["st"] for i in items), file=sys.stderr)
for i in items:
    print(f'{i["st"]:8} {i["k"]:40} {i["name"]}', file=sys.stderr)
