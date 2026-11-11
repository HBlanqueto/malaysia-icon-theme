#!/usr/bin/env python3
"""Generate the full-color icons: places (folders), file types and devices.

Figures come from the symbolic sources (src/malaysia-symbolic), so a new folder or file type
needs no drawing of its own: add a row to FOLDERS or MIMETYPES. App icons are the desktop's
own files, copied unchanged from src/apps.

Usage:
  python3 tools/color/build.py                 write Malaysia/ (light) and Malaysia-Dark/ (dark)
  python3 tools/color/build.py --check         fail if a generated file is out of date
  python3 tools/color/build.py --tint '#e8a33d' --out ~/.local/share/icons/Malaysia-Tinted
                                               write a theme tinted with that accent
                                               (inherits Malaysia; folders only)
"""
import argparse, colorsys, os, re, sys

import devices

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SYM = os.path.join(ROOT, "src", "malaysia-symbolic")
APP_ART = os.path.join(ROOT, "src", "apps")  # app icons drawn by the desktop, installed as they are


def glyph(name):
    """`d` of a symbolic source that has a single path."""
    for ctx in os.listdir(SYM):
        p = os.path.join(SYM, ctx, f"{name}-symbolic.svg")
        if os.path.exists(p):
            ds = re.findall(r' d="([^"]+)"', open(p, encoding="utf-8").read())
            if len(ds) != 1:
                sys.exit(f"{name}-symbolic has {len(ds)} paths; add a single stroke to EXTRA instead")
            return ds[0]
    sys.exit(f"src/malaysia-symbolic/*/{name}-symbolic.svg does not exist")


# Strokes on the 16 px grid that are not theme symbols yet.
EXTRA = {
    "note": "M6 12.5V4l7-1.5v8.5M6 12.5a1.8 1.8 0 1 1-3.6 0a1.8 1.8 0 0 1 3.6 0M13 11a1.8 1.8 0 1 1-3.6 0a1.8 1.8 0 0 1 3.6 0",
    "lines": "M4.5 4.5h7M4.5 7h7M4.5 9.5h7M4.5 12h4",
    "box": "M2.5 5 8 2.5 13.5 5v6L8 13.5 2.5 11zM2.5 5 8 7.5 13.5 5M8 7.5v6",
    "sheet": "M2.5 3.5h11v9h-11zM2.5 6.5h11M2.5 9.5h11M6.5 3.5v9",
    "easel": "M2.5 3.5h11v7h-11zM8 10.5v3M5.5 13.5h5",
    "letter-a": "M4 13 8 3l4 10M5.5 9.5h5",
    "puzzle": "M3 5.5h2.5a1.5 1.5 0 1 1 3 0H11v2.5a1.5 1.5 0 1 1 0 3V13H3z",
    "terminal": "M3.5 5l3 3-3 3M8 11.5h4.5",
    "chip": "M4.5 4.5h7v7h-7zM6.5 2.5v2M9.5 2.5v2M6.5 11.5v2M9.5 11.5v2M2.5 6.5h2M2.5 9.5h2M11.5 6.5h2M11.5 9.5h2",
    "apps": "M3 3h4v4H3zM9 3h4v4H9zM3 9h4v4H3zM9 9h4v4H9z",
    "symlink": "M3.5 12.5v-3a3 3 0 0 1 3-3h6M9.5 3.5l3 3-3 3",
    "shapes": "M6 8.5a3 3 0 1 0 0-6a3 3 0 0 0 0 6M8.5 8.5h5v5h-5z",
    "eye": "M1.5 8s2.5-4.5 6.5-4.5S14.5 8 14.5 8s-2.5 4.5-6.5 4.5S1.5 8 1.5 8zM8 10a2 2 0 1 0 0-4a2 2 0 0 0 0 4",
    "playlist": "M2.5 4h8M2.5 7.5h8M2.5 11h4.5M12.5 12.5V7l2-.5M12.5 12.5a1.5 1.5 0 1 1-3 0a1.5 1.5 0 0 1 3 0",
    "code": "M5.5 4.5 2 8l3.5 3.5M10.5 4.5 14 8l-3.5 3.5",
    "braces": "M6 2.5c-1.4 0-2 .6-2 2V6c0 1.2-.6 2-1.5 2 .9 0 1.5.8 1.5 2v1.5c0 1.4.6 2 2 2M10 2.5c1.4 0 2 .6 2 2V6"
              "c0 1.2.6 2 1.5 2-.9 0-1.5.8-1.5 2v1.5c0 1.4-.6 2-2 2",
    "database": "M3 4c0-1 2.2-1.8 5-1.8s5 .8 5 1.8v8c0 1-2.2 1.8-5 1.8S3 13 3 12zM3 4c0 1 2.2 1.8 5 1.8S13 5 13 4"
                "M3 8c0 1 2.2 1.8 5 1.8S13 9 13 8",
    "cloud": "M4.5 12.5a3 3 0 0 1-.3-6a4 4 0 0 1 7.6-1a3.5 3.5 0 0 1 .7 7z",
    "lock-open": "M4 7.5h8v6H4zM5.5 7.5v-2a2.5 2.5 0 0 1 4.8-1",
    "mail": "M2.5 4.5h11v8h-11zM2.5 5l5.5 4.5L13.5 5",
    "book": "M8 4.5C6.5 3.5 4.5 3 2.5 3v9.5c2 0 4 .5 5.5 1.5 1.5-1 3.5-1.5 5.5-1.5V3c-2 0-4 .5-5.5 1.5zM8 4.5v9.5",
    "branch": "M5 2.5v11M5 11c0-3.5 6-2.5 6-6.5M11 4.5a1.5 1.5 0 1 0 0-3a1.5 1.5 0 0 0 0 3",
    "gamepad": "M5 4.5h6a3 3 0 0 1 3 3l.5 3.5a1.6 1.6 0 0 1-2.8 1.2L10 10.5H6l-1.7 1.7A1.6 1.6 0 0 1 1.5 11L2 7.5a3 3 0 0 1 3-3z"
               "M5.5 6.5v2M4.5 7.5h2M10.5 7.5h.01",
    "clock": "M8 14a6 6 0 1 0 0-12a6 6 0 0 0 0 12M8 4.5V8l2.5 1.5",
    "trash": "M3 4.5h10M6 4.5V3h4v1.5M4.5 4.5l.7 9h5.6l.7-9",
    "chart": "M2.5 13.5h11M4.5 13.5v-4M8 13.5v-9M11.5 13.5v-6",
    "pencil": "M3 13l.8-3.3 7-7 2.5 2.5-7 7zM9.3 4.2l2.5 2.5",
    "brush": "M13.5 2.5 8 8M8 8l-1.5-1.5M6.5 9.5a2 2 0 0 0-2.8 0C2.5 10.7 3.2 12.4 2.5 13.5c1.6 0 3.5.2 4.6-.9a2 2 0 0 0 0-2.8z",
    "mic": "M8 2.5a2 2 0 0 0-2 2V8a2 2 0 0 0 4 0V4.5a2 2 0 0 0-2-2zM4.5 8a3.5 3.5 0 0 0 7 0M8 11.5v2",
    "calculator": "M4 2.5h8v11H4zM5.5 4.5h5V7h-5zM6 9.5h.01M8 9.5h.01M10 9.5h.01M6 11.5h.01M8 11.5h.01M10 11.5h.01",
    "exclaim": "M8 3v6.5M8 12.5v.01",
    "calendar": "M2.5 4h11v9.5h-11zM2.5 7h11M5.5 2.5V5M10.5 2.5V5",
    "key": "M6 10.5a3 3 0 1 1 2.6-1.5L13 13.5M11 11.5l1.5-1.5",
    "disc": "M8 14a6 6 0 1 0 0-12a6 6 0 0 0 0 12M8 9.5a1.5 1.5 0 1 0 0-3a1.5 1.5 0 0 0 0 3",
    "palette": "M8 2.5a5.5 5.5 0 0 0 0 11c1 0 1.2-.8.8-1.5-.5-.8 0-1.8 1-1.8h1.4a2.3 2.3 0 0 0 2.3-2.3C13.5 4.8 11 2.5 8 2.5z"
               "M5 8h.01M6.5 5.5h.01M9.5 5h.01",
}
G = lambda n: EXTRA[n] if n in EXTRA else glyph(n)
INK = "#8b9098"

# name → figure (None = plain folder)
FOLDERS = {
    "folder": None, "inode-directory": None, "folder-drag-accept": "open",
    "folder-documents": "text-x-generic", "folder-download": "arrow-down", "folder-music": "note",
    "folder-pictures": "photo", "folder-images": "photo", "folder-videos": "video-x-generic",
    "folder-projects": "text-x-script", "folder-publicshare": "avatar-default", "folder-public": "avatar-default",
    "folder-remote": "network-workgroup", "folder-templates": "edit-copy", "user-desktop": "video-display",
    "user-home": "go-home", "user-bookmarks": "user-bookmarks", "folder-bookmark": "user-bookmarks",
    "folder-cloud": "cloud", "folder-code": "code", "folder-development": "code", "folder-database": "database",
    "folder-locked": "system-lock-screen", "folder-encrypted": "system-lock-screen",
    "folder-unlocked": "lock-open", "folder-decrypted": "lock-open", "folder-git": "branch", "folder-mail": "mail",
    "folder-notes": "pencil", "folder-important": "exclaim", "folder-book": "book", "folder-library": "book",
    "folder-games": "gamepad", "folder-print": "printer", "folder-presentation": "easel", "folder-table": "sheet",
    "folder-chart": "chart", "folder-script": "terminal", "folder-temp": "clock", "folder-trash": "trash",
    "folder-root": "emblem-system", "folder-log": "lines", "folder-build": "preferences-system", "folder-design": "shapes",
    "folder-drawing": "pencil", "folder-paint": "palette", "folder-language": "network-workgroup",
    "folder-podcast": "mic", "folder-extension": "puzzle", "folder-calculate": "calculator", "folder-tar": "box",
}
# folder-<color>: plain folders in the macOS tag colors
FOLDER_COLORS = {
    "red": "#ff3b30", "orange": "#ff9500", "yellow": "#ffcc00", "green": "#34c759", "cyan": "#32ade6",
    "blue": "#007aff", "purple": "#af52de", "pink": "#ff2d55", "brown": "#a2845e", "grey": "#8e8e93", "black": "#3a3a3c",
}


def family(style, fig, color, names):
    """{icon name: extension} → MIMETYPES rows that share a style, figure and color."""
    return {name: (fig, color, text, style) for name, text in names.items()}


# language → (color, extension); every source file is a tile with the code figure
CODE = {
    "text-x-python": ("#3572a5", "PY"), "text-x-python3": ("#3572a5", "PY"), "application-javascript": ("#d4a90a", "JS"),
    "text-javascript": ("#d4a90a", "JS"), "text-x-javascript": ("#d4a90a", "JS"), "text-x-typescript": ("#3178c6", "TS"),
    "application-x-typescript": ("#3178c6", "TS"), "text-x-csrc": ("#555b66", "C"), "text-x-c": ("#555b66", "C"),
    "text-x-chdr": ("#555b66", "H"), "text-x-c++src": ("#e0457b", "C++"), "text-x-cpp": ("#e0457b", "C++"),
    "text-x-c++hdr": ("#e0457b", "HPP"), "text-x-csharp": ("#178600", "C#"), "text-x-go": ("#00a2c7", "GO"),
    "text-x-java": ("#b07219", "JAVA"), "application-x-java": ("#b07219", "CLASS"), "text-x-kotlin": ("#8f5cf0", "KT"),
    "text-rust": ("#ce422b", "RS"), "text-x-rust": ("#ce422b", "RS"), "application-x-ruby": ("#cc342d", "RB"),
    "text-x-ruby": ("#cc342d", "RB"), "application-x-php": ("#4f5d95", "PHP"), "text-x-php": ("#4f5d95", "PHP"),
    "text-x-lua": ("#2c2d72", "LUA"), "application-x-perl": ("#39457e", "PL"), "text-x-perl": ("#39457e", "PL"),
    "text-x-scala": ("#c22d40", "SCALA"), "text-x-vala": ("#7b52c4", "VALA"), "text-x-haskell": ("#5e5086", "HS"),
    "text-x-r": ("#1a7fd4", "R"), "text-x-tcl": ("#a3392f", "TCL"), "text-x-pascal": ("#b8722c", "PAS"),
    "text-x-fortran": ("#4d41b1", "F"), "text-x-cobol": ("#3b5a7a", "COBOL"), "text-x-emacs-lisp": ("#7f5ab6", "EL"),
    "text-x-qml": ("#2e9b49", "QML"), "application-x-gdscript": ("#478cbf", "GD"), "text-x-makefile": ("#5f6570", "MAKE"),
    "text-x-cmake": ("#2f6db5", "CMAKE"), "text-x-patch": ("#5f6570", "DIFF"), "text-css": ("#663399", "CSS"),
    "text-x-sass": ("#c6538c", "SASS"), "text-x-scss": ("#c6538c", "SCSS"), "text-less": ("#1d365d", "LESS"),
    "text-xml": ("#e0632a", "XML"), "application-xml": ("#e0632a", "XML"), "text-yaml": ("#cb171e", "YAML"),
    "application-yaml": ("#cb171e", "YAML"), "application-toml": ("#9c4221", "TOML"), "text-x-tex": ("#3d6117", "TEX"),
    "text-x-typst": ("#239dad", "TYP"), "text-x-meson": ("#4a3f8f", "MESON"), "text-x-nix": ("#5277c3", "NIX"),
}
MIMETYPES = {
    **{name: ("code", color, text, "tile") for name, (color, text) in CODE.items()},
    "text-x-script": ("text-x-script", "#2a2d33", "CODE", "tile"),
    "text-html": ("network-workgroup", "#e0632a", "HTML", "tile"),
    **family("tile", "braces", "#5f6570", {"application-json": "JSON", "application-ld+json": "JSON"}),
    **family("tile", "terminal", "#2a2d33", {"application-x-shellscript": "SH", "text-x-shellscript": "SH",
                                             "application-x-bat": "BAT", "application-x-executable": "EXEC"}),
    **family("tile", "database", "#2f6db5", {"application-sql": "SQL", "text-x-sql": "SQL",
                                             "application-vnd.sqlite3": "DB", "application-x-sqlite3": "DB"}),
    **family("text", None, INK, {"text-x-generic": "TXT", "text-plain": "TXT", "text-x-log": "LOG",
                                  "text-x-readme": "README", "text-x-copying": "LICENSE", "text-x-authors": "AUTHORS",
                                  "text-x-changelog": "CHANGES", "text-x-install": "INSTALL", "text-markdown": "MD",
                                  "text-x-markdown": "MD", "text-richtext": "RTF", "text-x-gettext-translation": "PO",
                                  "text-x-gettext-translation-template": "POT", "text-csv": "CSV",
                                  "text-x-generic-template": "TXT"}),
    "text-x-preview": ("eye", "#6b7280", "TXT", "tile"),
    **family("tile", "media-view-subtitles", "#5f6570", {"application-x-subrip": "SRT", "text-x-subrip": "SRT",
                                                         "text-vtt": "VTT", "text-x-ssa": "ASS"}),
    **family("tile", "photo", "#0f97bd", {"image-x-generic": "IMAGE", "image-png": "PNG", "image-jpeg": "JPG",
                                          "image-gif": "GIF", "image-webp": "WEBP", "image-bmp": "BMP",
                                          "image-tiff": "TIFF", "image-heif": "HEIC", "image-avif": "AVIF",
                                          "image-vnd.microsoft.icon": "ICO", "image-x-xcf": "XCF",
                                          "image-x-compressed-xcf": "XCF", "image-vnd.djvu": "DJVU"}),
    **family("tile", "shapes", "#c13fc9", {"image-svg+xml": "SVG", "image-svg+xml-compressed": "SVGZ",
                                           "application-postscript": "EPS", "x-office-drawing": "ODG",
                                           "x-office-drawing-template": "OTG",
                                           "application-vnd.oasis.opendocument.graphics": "ODG"}),
    **family("tile", "note", "#e2306e", {"audio-x-generic": "AUDIO", "audio-mpeg": "MP3", "audio-x-wav": "WAV",
                                         "audio-flac": "FLAC", "audio-ogg": "OGG", "audio-x-vorbis+ogg": "OGG",
                                         "audio-x-opus+ogg": "OPUS", "audio-mp4": "M4A", "audio-aac": "AAC",
                                         "audio-midi": "MIDI", "audio-x-aiff": "AIFF"}),
    **family("tile", "playlist", "#e2306e", {"audio-x-mpegurl": "M3U", "audio-x-mp3-playlist": "M3U",
                                              "audio-x-scpls": "PLS"}),
    **family("tile", "media-playback-start", "#6b4fd8", {"video-x-generic": "VIDEO", "video-mp4": "MP4",
                                                         "video-x-matroska": "MKV", "video-webm": "WEBM",
                                                         "video-quicktime": "MOV", "video-x-msvideo": "AVI",
                                                         "video-mpeg": "MPEG", "video-ogg": "OGV",
                                                         "application-x-flash-video": "FLV"}),
    **family("tile", "letter-a", "#5f6570", {"font-x-generic": "FONT", "font-ttf": "TTF", "font-otf": "OTF",
                                             "font-woff": "WOFF", "font-woff2": "WOFF2", "font-collection": "TTC"}),
    **family("page", "lines", "#1e6fe0", {"x-office-document": "DOC", "x-office-document-template": "DOT",
                                          "application-msword": "DOC", "application-msword-template": "DOT",
                                          "application-vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",
                                          "application-vnd.oasis.opendocument.text": "ODT",
                                          "application-vnd.oasis.opendocument.text-template": "OTT",
                                          "application-rtf": "RTF"}),
    **family("page", "sheet", "#1f9a46", {"x-office-spreadsheet": "XLS", "x-office-spreadsheet-template": "XLT",
                                          "application-vnd.ms-excel": "XLS",
                                          "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
                                          "application-vnd.oasis.opendocument.spreadsheet": "ODS",
                                          "application-vnd.oasis.opendocument.spreadsheet-template": "OTS"}),
    **family("page", "easel", "#e86a10", {"x-office-presentation": "PPT", "x-office-presentation-template": "POT",
                                          "application-vnd.ms-powerpoint": "PPT",
                                          "application-vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX",
                                          "application-vnd.oasis.opendocument.presentation": "ODP",
                                          "application-vnd.oasis.opendocument.presentation-template": "OTP"}),
    **family("page", "text-x-generic", "#e0321f", {"application-pdf": "PDF", "application-x-pdf": "PDF"}),
    **family("page", "book", "#e86a10", {"application-epub+zip": "EPUB", "application-x-mobipocket-ebook": "MOBI",
                                         "application-x-fictionbook+xml": "FB2"}),
    **family("tile", "calendar", "#e0321f", {"x-office-calendar": "ICS", "text-calendar": "ICS"}),
    **family("tile", "avatar-default", "#e0632a", {"x-office-addressbook": "VCF", "text-vcard": "VCF",
                                                   "text-x-vcard": "VCF"}),
    **family("tile", "mail", "#1e7bf2", {"message-rfc822": "EML", "application-mbox": "MBOX",
                                         "message-news": "NEWS"}),
    **family("zip", None, "#c98a2b", {"package-x-generic": "PKG", "application-zip": "ZIP", "application-x-zip": "ZIP",
                                      "application-x-zip-compressed": "ZIP", "application-x-tar": "TAR",
                                      "application-x-compressed-tar": "TGZ", "application-gzip": "GZ",
                                      "application-x-gzip": "GZ", "application-x-bzip": "BZ2",
                                      "application-x-bzip2": "BZ2", "application-x-bzip-compressed-tar": "TBZ",
                                      "application-x-xz": "XZ", "application-x-xz-compressed-tar": "TXZ",
                                      "application-x-lzma": "LZMA", "application-x-lzma-compressed-tar": "TLZ",
                                      "application-x-lzip": "LZ", "application-x-7z-compressed": "7Z",
                                      "application-vnd.rar": "RAR", "application-x-rar": "RAR",
                                      "application-zstd": "ZST", "application-x-zstd-compressed-tar": "TZST",
                                      "application-x-archive": "AR", "application-x-cpio": "CPIO",
                                      "application-vnd.ms-cab-compressed": "CAB", "application-x-arj": "ARJ",
                                      "application-x-java-archive": "JAR"}),
    **family("tile", "box", "#b07d12", {"x-package-repository": "REPO", "application-x-deb": "DEB",
                                        "application-vnd.debian.binary-package": "DEB", "application-x-rpm": "RPM",
                                        "application-x-alpm-package": "PKG", "application-vnd.flatpak": "FLATPAK",
                                        "application-vnd.flatpak.ref": "FLATPAK", "application-vnd.flatpak.repo": "REPO",
                                        "application-vnd.snap": "SNAP", "application-x-msi": "MSI",
                                        "model": "3D", "model-stl": "STL", "model-obj": "OBJ",
                                        "model-gltf-binary": "GLB", "model-gltf+json": "GLTF"}),
    **family("tile", "apps", "#1e7bf2", {"application-x-generic": "APP", "application-vnd.appimage": "APPIMAGE",
                                         "application-x-desktop": "DESKTOP", "application-x-ms-dos-executable": "EXE",
                                         "application-vnd.microsoft.portable-executable": "EXE",
                                         "application-x-msdownload": "EXE"}),
    **family("tile", "disc", "#7a808a", {"application-x-cd-image": "ISO", "application-vnd.efi.iso": "ISO",
                                         "application-x-raw-disk-image": "IMG", "application-x-qemu-disk": "QCOW2"}),
    **family("tile", "chip", "#5f6570", {"application-x-firmware": "FW", "application-x-sharedlib": "LIB",
                                         "application-x-object": "O", "application-octet-stream": "BIN"}),
    **family("tile", "system-lock-screen", "#b07d12", {"application-certificate": "CERT",
                                                       "application-pkix-cert": "CRT", "application-x-x509-ca-cert": "CRT"}),
    **family("tile", "key", "#b07d12", {"application-pgp-signature": "SIG", "application-pgp-encrypted": "PGP",
                                        "application-pgp-keys": "KEY", "application-x-pem-key": "PEM"}),
    **family("tile", "arrow-down", "#2e9b49", {"application-x-bittorrent": "TORRENT",
                                              "application-x-partial-download": "PART"}),
    "application-x-addon": ("puzzle", "#6b4fd8", "ADDON", "tile"),
    "application-x-theme": ("palette", "#c13fc9", "THEME", "tile"),
    "inode-symlink": ("symlink", "#7a808a", "LINK", "tile"),
    "unknown": ("dialog-question", "#7a808a", "", "tile"),
}
TEMPLATES = {k for k in MIMETYPES if k.endswith("-template")}

# Stroked letters in a box 6 units tall: (advance width, path). An icon with <text> renders
# with whatever font each system has, so labels are drawn instead.
LETTERS = {
    "A": (4, "M0 6 2 0l2 6M.7 4h2.6"), "B": (3.8, "M0 3h2.3a1.5 1.5 0 0 1 0 3H0V0h2a1.5 1.5 0 0 1 0 3"), "C": (4, "M4 1A2.4 3 0 1 0 4 5"),
    "D": (4, "M0 0v6h1.4A2.6 3 0 0 0 1.4 0z"), "E": (3.6, "M3.6 0H0v6h3.6M0 3h3"),
    "F": (3.6, "M3.6 0H0v6M0 3h3"), "G": (4, "M4 1A2.4 3 0 1 0 4 5V3.4H2.4"),
    "H": (4, "M0 0v6M4 0v6M0 3h4"), "I": (0, "M0 0v6"), "K": (4, "M0 0v6M4 0 0 3.8M1.5 2.6 4 6"),
    "L": (3.4, "M0 0v6h3.4"), "M": (5, "M0 6V0l2.5 4L5 0v6"), "N": (4, "M0 6V0l4 6V0"),
    "O": (4, "M2 0A2 3 0 1 0 2 6A2 3 0 1 0 2 0z"), "P": (3.8, "M0 6V0h2.2a1.6 1.6 0 0 1 0 3.2H0"),
    "R": (3.8, "M0 6V0h2.2a1.6 1.6 0 0 1 0 3.2H0M2.2 3.2 3.8 6"),
    "S": (3.8, "M3.6.9C3.2.3 2.7 0 1.9 0 .9 0 .2.6.2 1.5c0 2 3.6 1.1 3.6 3 0 .9-.8 1.5-1.9 1.5-.9 0-1.6-.4-1.9-1"),
    "T": (4, "M0 0h4M2 0v6"), "U": (4, "M0 0v4a2 2 0 0 0 4 0V0"), "V": (4, "M0 0l2 6 2-6"),
    "W": (5.4, "M0 0l1.3 6L2.7 1.8 4.1 6 5.4 0"), "X": (4, "M0 0l4 6M4 0 0 6"),
    "3": (3.6, "M.2 0h3.2L1.6 2.4h.4a1.8 1.8 0 1 1-1.8 2.6"),
    "J": (3.2, "M3.2 0v4.4a1.6 1.6 0 0 1-3.2 0"), "Q": (4, "M2 0A2 3 0 1 0 2 6A2 3 0 1 0 2 0zM2.6 4.4 4 6"),
    "Y": (4, "M0 0l2 3 2-3M2 3v3"), "Z": (3.8, "M0 0h3.8L0 6h3.8"),
    "0": (3.6, "M1.8 0A1.8 3 0 1 0 1.8 6A1.8 3 0 1 0 1.8 0z"), "1": (1.6, "M0 1.2 1.6 0v6"),
    "2": (3.6, "M.1 1.4A1.7 1.6 0 0 1 3.4 1.6c0 1.6-3.4 2.6-3.4 4.4h3.6"), "4": (3.8, "M2.8 6V0L0 4.2h3.8"),
    "7": (3.6, "M0 0h3.6L1.2 6"), "+": (3.6, "M1.8 1.2v3.6M0 3h3.6"),
    "#": (4, "M1.4.6 1 5.4M3.2.6l-.4 4.8M0 2.2h4M0 3.8h4"),
}


def label(text, cx, top, height, color):
    s, gap = height / 6, 1.25
    widths = [LETTERS[c][0] for c in text]
    total = (sum(widths) + gap * (len(text) - 1)) * s
    x, out = cx - total / 2, []
    for c, w in zip(text, widths):
        out.append(f'<path transform="translate({x:.2f} {top}) scale({s:.4f})" d="{LETTERS[c][1]}"/>')
        x += (w + gap) * s
    return (f'<g fill="none" stroke="{color}" stroke-width="{1.05 / s:.3f}" stroke-linecap="round" '
            f'stroke-linejoin="round">' + "".join(out) + "</g>")


def shade(hex_, pct):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    f = pct / 100
    ch = lambda v: round(min(255, max(0, v * (1 + f) if f < 0 else v + (255 - v) * f)))
    return "#" + "".join(f"{ch(v):02x}" for v in (r, g, b))


def palette(variant, tint=None):
    if variant == "light":
        return dict(back=("#58a6ee", "#2f7fd6"), front=("#9ad2fb", "#5fb0f2"), glyph="#1f62ad", hi=.65)
    if variant == "dark":
        return dict(back=("#2d6fbf", "#1c4f8e"), front=("#5b9fe3", "#3a7ecb"), glyph="#123b6c", hi=.35)
    # tinted: the dark variant's lightness with the accent's hue
    h, l, s = colorsys.rgb_to_hls(*(int(tint[i:i + 2], 16) / 255 for i in (1, 3, 5)))
    def hls(l2, s2):
        return "#" + "".join(f"{round(v * 255):02x}" for v in colorsys.hls_to_rgb(h, l2, min(1, s2)))
    return dict(back=(hls(.46, s * .75), hls(.34, s * .75)), front=(hls(.66, s * .85), hls(.52, s * .85)),
                glyph=hls(.22, s * .8), hi=.35)


def svg(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 64 64">'
            f'<defs>{devices.DROP}{defs}</defs><g filter="url(#drop)">{body}</g></svg>\n')


def grad(id_, a, b, x2=0):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')


def emboss(d, x, y, k, color, alpha):
    common = f'fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="{d}"'
    return (f'<g transform="translate({x} {y}) scale({k})">'
            f'<path stroke="#ffffff" stroke-opacity=".45" transform="translate(0 .5)" {common}/>'
            f'<path stroke="{color}" stroke-opacity="{alpha}" {common}/></g>')


FOLD = ('<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1"><stop offset=".8" stop-color="#000000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000000" stop-opacity=".14"/></linearGradient>')


def folder(fig, p):
    """A macOS-style folder: no outline; a lit top edge, a shaded bottom edge and a pressed-in figure."""
    defs = grad("back", *p["back"]) + grad("front", *p["front"]) + FOLD
    back = '<path fill="url(#back)" d="M5 15a4 4 0 0 1 4-4h14.5l5 5H55a4 4 0 0 1 4 4v28a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/>'
    if fig == "open":  # the front leans forward
        d = "M11.2 24h46.9a3 3 0 0 1 2.9 3.7l-4.6 20.5A4.5 4.5 0 0 1 52 52H9a3.6 3.6 0 0 1-3.5-4.4l4.4-20.8A3.6 3.6 0 0 1 11.2 24z"
        return svg(back + f'<path fill="url(#front)" d="{d}"/><path fill="url(#edge)" d="{d}"/>'
                   f'<path d="M11.4 24.7h46.3" stroke="#ffffff" stroke-opacity="{p["hi"]}" stroke-width=".9" stroke-linecap="round"/>', defs)
    d = "M5 23a4 4 0 0 1 4-4h46a4 4 0 0 1 4 4v25a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"
    front = (f'<path fill="url(#front)" d="{d}"/><path fill="url(#edge)" d="{d}"/>'
             f'<path d="M8.6 19.6h46.8" stroke="#ffffff" stroke-opacity="{p["hi"]}" stroke-width=".9" stroke-linecap="round"/>')
    return svg(back + front + (emboss(G(fig), 22, 25.5, 1.25, p["glyph"], .75) if fig else ""), defs)


PAGE = "M14 4h23l13 13v41a2 2 0 0 1-2 2H14a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"
CORNER = "M37 4v10a3 3 0 0 0 3 3h10z"


def glyph_at(fig, cx, cy, k, color, width=1.6):
    return (f'<g transform="translate({cx - 8 * k:g} {cy - 8 * k:g}) scale({k:g})"><path fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" d="{G(fig)}"/></g>')


def document(fig, color, text, style, template):
    """A macOS-style document: a sheet with a folded corner and a hairline edge.

    tile: white sheet, a colored tile with the figure, the extension in gray.
    page: a sheet in the type's color, a large white figure and white extension.
    zip:  a colored sheet with a zipper down from the top.
    text: white sheet with lines of text.
    """
    white = style in ("tile", "text")
    top, bottom = ("#ffffff", "#f1f2f5") if white else (shade(color, 18), color)
    defs = (grad("page", top, bottom) + grad("tile", shade(color, 28), color)
            + grad("fold", "#ffffff" if white else shade(color, 45), "#dfe2e8" if white else shade(color, 8), 1))
    sheet = (f'<path fill="url(#page)" d="{PAGE}"/>'
             f'<path fill="none" stroke="#000000" stroke-opacity=".1" stroke-width=".5" d="{PAGE}"/>')
    stack = "".join(f'<g transform="translate({o} {o})" opacity="{a}">{sheet}</g>' for o, a in ((3, .5), (1.5, .8))) if template else ""
    fold = (f'<path d="{CORNER}" fill="#000000" fill-opacity=".14" transform="translate(-.8 .9)"/>'
            f'<path d="{CORNER}" fill="url(#fold)"/>')
    ink = INK if white else "#ffffff"
    if style == "tile":
        art = (f'<rect x="21" y="16" width="22" height="22" rx="5.6" fill="url(#tile)"/>'
               f'<rect x="21" y="16" width="22" height="11" rx="5.6" fill="#ffffff" fill-opacity=".12"/>'
               + glyph_at(fig, 32, 27, 1.05, "#ffffff"))
    elif style == "page":
        art = glyph_at(fig, 31, 29, 1.45, "#ffffff", 1.4)
    elif style == "zip":
        teeth = "".join(f'<rect x="{30 if i % 2 else 32}" y="{4 + i * 2.2:.1f}" width="2" height="1.4" rx=".3" fill="#ffffff" fill-opacity=".85"/>'
                        for i in range(10))
        art = (teeth + '<rect x="29.4" y="26" width="5.2" height="8.6" rx="1.4" fill="#ffffff" fill-opacity=".9"/>'
               + f'<rect x="30.9" y="30.4" width="2.2" height="2.6" rx=".6" fill="{color}"/>')
    else:
        art = "".join(f'<path d="M18 {14 + i * 3.4:.1f}h{w}" stroke="#b3b8c0" stroke-width="1.2" stroke-linecap="round"/>'
                      for i, w in enumerate((15, 15, 26, 22, 26, 26, 14, 24)))
    return svg(stack + sheet + fold + art + (label(text, 31, 47.5, 4.6, ink) if text else ""), defs)


CONTEXTS = {"places": "Places", "mimetypes": "MimeTypes", "status": "Status"}
# scalable/status only holds folder-open, which meson installs as a link to places/folder.svg
VARIANT_DIRS = ["scalable/mimetypes", "scalable/places", "scalable/status"]


def theme_index(name, comment, inherits, dirs):
    s = (f"[Icon Theme]\nName={name}\nComment={comment}\nExample=folder\nInherits={inherits}\n\n"
         f"Directories={','.join(dirs)}\n")
    for d in dirs:
        s += f"\n[{d}]\nContext={CONTEXTS[d.split('/')[1]]}\nSize=128\nMinSize=8\nMaxSize=512\nType=Scalable\n"
    return s


def files(variant, tint=None):
    p = palette(variant, tint)
    out = {}
    for name, fig in FOLDERS.items():
        ctx = "mimetypes" if name.startswith("inode-") else "places"
        out[f"scalable/{ctx}/{name}.svg"] = folder(fig, p)
    if variant == "dark":
        for name, svg_ in devices.trash_icons(dark=True).items():
            out[f"scalable/places/{name}.svg"] = svg_
    if variant == "light":
        for f in sorted(os.listdir(APP_ART)):
            out[f"scalable/apps/{f}"] = open(os.path.join(APP_ART, f), encoding="utf-8").read()
        for name, svg_ in devices.icons(G, label).items():
            out[f"scalable/devices/{name}.svg"] = svg_
        for name, (fig, color, text, style) in MIMETYPES.items():
            out[f"scalable/mimetypes/{name}.svg"] = document(fig, color, text, style, name in TEMPLATES)
        for color, hex_ in FOLDER_COLORS.items():
            out[f"scalable/places/folder-{color}.svg"] = folder(None, palette("tinted", hex_))
        for name, svg_ in devices.places().items():
            out[f"scalable/places/{name}.svg"] = svg_
        for name, svg_ in devices.status(G).items():
            out[f"scalable/status/{name}.svg"] = svg_
    return out


def sync(base, wanted, check, index=None):
    stale = []
    if index:
        wanted = {**wanted, "index.theme": index}
    for rel, content in wanted.items():
        p = os.path.join(base, rel)
        if not os.path.exists(p) or open(p, encoding="utf-8").read() != content:
            stale.append(os.path.relpath(p, ROOT) if p.startswith(ROOT) else p)
            if not check:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "w", encoding="utf-8").write(content)
    return stale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--tint")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.tint:
        if not (a.out and re.fullmatch(r"#[0-9a-fA-F]{6}", a.tint)):
            sys.exit("--tint needs a #rrggbb color and --out")
        out = os.path.expanduser(a.out)
        sync(out, files("tinted", a.tint.lower()), False,
             theme_index(os.path.basename(out.rstrip("/")), f"Malaysia folders tinted {a.tint}", "Malaysia",
                         VARIANT_DIRS))
        os.makedirs(os.path.join(out, "scalable", "status"), exist_ok=True)
        link = os.path.join(out, "scalable", "status", "folder-open.svg")
        if not os.path.lexists(link):
            os.symlink("../places/folder.svg", link)
        print(f"tinted theme written to {out}")
        return
    stale = sync(os.path.join(ROOT, "Malaysia"), files("light"), a.check)
    stale += sync(os.path.join(ROOT, "Malaysia-Dark"), files("dark"), a.check,
                  theme_index("Malaysia-Dark", "Malaysia with dark folders and trash", "Malaysia",
                              VARIANT_DIRS))
    if a.check:
        sys.exit("out of date:\n  " + "\n  ".join(stale)) if stale else print("up to date")
    else:
        print(f"{len(stale)} files written")


if __name__ == "__main__":
    main()
