# Malaysia Icon Theme

Icon theme for the [Malaysia](https://github.com/HBlanqueto/malaysia) Wayland desktop.

Malaysia started as a fork of the [Adwaita icon theme](https://gitlab.gnome.org/GNOME/adwaita-icon-theme)
51.0. It now ships only the icons it keeps or redraws and inherits everything else:

```ini
[Icon Theme]
Name=Malaysia
Inherits=Adwaita,hicolor
```

An icon that is not in `Malaysia/` is looked up in Adwaita (and, through Adwaita, in
AdwaitaLegacy) and then in hicolor. The `adwaita-icon-theme` package therefore has to
be installed next to this one.

## Layout

```
Malaysia/
├── scalable/   full-color SVG: devices, mimetypes, places, status (apps later)
└── symbolic/   recolorable SVG: actions, categories, devices, mimetypes, places, status, ui
src/            Inkscape sources inherited from Adwaita (fullcolor/*.source.svg, symbolic/core.svg)
docs/           icon map and the Malaysia Icons 2 proposal
tools/          generators for the pages in docs/
```

Compared with Adwaita 51.0, phase 1 of the proposal removed `16x16/` (PNG copies of the
scalable icons), `symbolic/legacy/` and `symbolic/emotes/`. All three still resolve through
the `Adwaita` parent theme.

## Desktop symbols

The Malaysia desktop draws its own symbols in code: the `Symbol` enum in barrierkit
(`crates/bk/src/symbol.rs`) and the menu icons in malaysia-shell (`src/menubar/icons.rs`).
Phase 2 brought those 97 symbols into the theme under their freedesktop names, so GTK and
Qt apps use the same glyphs as the desktop. `docs/symbols.md` lists every symbol with its
name in the theme.

- `src/malaysia-symbolic/<context>/<name>.svg` holds the editable sources, drawn with
  strokes on a 16 px grid (stroke width from barrierkit's `components.symbol.stroke`).
- `Malaysia/symbolic/<context>/<name>.svg` holds the exported icons. GTK forces `fill` on
  every `path`, `rect` and `circle` of a symbolic icon and ignores `stroke`, so the exporter
  turns every stroke into a filled outline.

```sh
pip install -r tools/requirements.txt
python3 tools/symbols/import_desktop.py <malaysia> <barrierkit>   # code → src/malaysia-symbolic
python3 tools/symbols/export.py                                   # src/malaysia-symbolic → Malaysia/symbolic
python3 tools/symbols/export.py --check                           # fails if an export is out of date
```

Edit a source in `src/malaysia-symbolic/` and run `export.py`; do not edit the exported
file. Running `import_desktop.py` again overwrites the sources with what the desktop code
draws.

## Folders and file types

Phase 3 replaced the full-color folders and file types with generated ones:

- **Folders** (14 in `scalable/places`, plus `inode-directory`): a blue folder with the
  folder's symbol embossed on the front. The symbol comes from `src/malaysia-symbolic`.
- **File types** (26, in `scalable/mimetypes`): a white page, the type's symbol, and a
  colored label. The label letters are stroked paths, not `<text>`, so they look the
  same without any font installed. Templates (`*-template`) get a dashed page edge.

`tools/color/build.py` writes all of them; to add a folder or a file type, add a row to
`FOLDERS` or `MIMETYPES` and run it. Do not edit the generated SVGs.

```sh
python3 tools/color/build.py            # Malaysia/ and Malaysia-Dark/
python3 tools/color/build.py --check    # fails if a generated file is out of date
python3 tools/color/build.py --tint '#e8a33d' --out ~/.local/share/icons/Malaysia-Tinted
```

Variants are separate themes, because an icon theme cannot change with the color scheme:

- `Malaysia` has the light folders.
- `Malaysia-Dark` (installed next to it, `Inherits=Malaysia`) has only the dark folders.
- A tinted theme is generated on demand with `--tint` from the user's accent color.

The Adwaita sources in `src/fullcolor/` for these icons are no longer used.
`network-server`, `network-workgroup` and `user-trash` are still Adwaita's drawings.

## Build and install

```sh
meson setup _build
meson install -C _build
```

This installs `Malaysia` and `Malaysia-Dark` to `$prefix/share/icons/` and refreshes their
icon caches.
To use it in the Malaysia desktop, set `MALAYSIA_ICON_THEME=Malaysia` for the launcher
and choose `Malaysia` as the GTK icon theme.

## Pages

- `docs/icon-map.html`: every icon in the theme, searchable. Regenerate with
  `python3 tools/build-icon-map.py`.
- `docs/propuesta-malaysia-icons.html`: the Malaysia Icons 2 proposal (in Spanish).
  Regenerate with `python3 tools/proposal/build.py <malaysia> <barrierkit>`.

## Symbolic icons and recoloring

GTK recolors symbolic icons at runtime: it wraps each one in a stylesheet that sets the
fill of every path and rectangle. Do not leave a path or rectangle without a fill or a
stroke on the assumption that it is invisible. To keep part of an icon in color, set
`class` on the shape or group to `warning`, `error` or `success`.

## License

Same as Adwaita: GNU LGPL v3 or Creative Commons Attribution-Share Alike 3.0 (see
`COPYING`). The artwork inherited from Adwaita is by the GNOME Project (see `AUTHORS`).
