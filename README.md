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
Malaysia/                the Malaysia theme
├── scalable/            full-color SVG: apps, devices, mimetypes, places, status
└── symbolic/            recolorable SVG: actions, categories, devices, mimetypes, places, status, ui
Malaysia-Dark/           child theme with the dark folders and app icons (generated)
src/
├── malaysia-symbolic/   stroke sources of the desktop symbols
├── fullcolor/           Adwaita's Inkscape sources (*.source.svg)
└── symbolic/            Adwaita's symbolic sheets (core.svg)
docs/                    symbols.md, icon map and the Malaysia Icons 2 proposal
tools/                   importers and generators
.github/workflows/       CI
```

Nothing is generated from `src/fullcolor/` or `src/symbolic/`. They stay as the editable
sources of the icons that are still Adwaita's drawings: about 500 symbols, the status icons
in `scalable/`, and `network-server`, `network-workgroup` and `user-trash`. Delete a source
once its icon is redrawn.

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

- `Malaysia` has the light folders and app icons.
- `Malaysia-Dark` (installed next to it, `Inherits=Malaysia`) has only the dark folders and
  app icons.
- A tinted theme is generated on demand with `--tint` from the user's accent color.

`network-server`, `network-workgroup` and `user-trash` are still Adwaita's drawings.

## Devices

The 23 icons in `scalable/devices` follow Apple's guidance for macOS icons (lifelike
rendering: a front-facing, level view, one consistent drop shadow, and physical materials
with mass) and the macOS 26.1 drive icon as the visual reference. No icon copies an Apple
drawing or logo.

- No outlines: edges come from light. Each body has a rounded side lit from the front (a
  thin highlight at the very edge, then a darker band), a beveled top edge and a darker
  bottom band the full width of the body.
- Marks are pressed into the surface with a soft inner shadow (`inset` filter), and every
  device casts the same shadow (`drop` filter).
- Devices show their working parts: the hard disk is an open drive with platter and
  actuator arm, the mouse has buttons and a scroll wheel, and screens show crystal blue
  glass.
- Finishes vary so the set does not read all light: aluminum and white plastic,
  glossy graphite (speaker, webcam, display, phone, tablet, e-reader, external drive,
  scanner base) and blue anodized aluminum (USB stick).
- `tools/color/devices.py` draws every device from these shared materials: aluminum,
  white plastic, graphite, steel, black glass, speaker mesh and crystal blue. Each device is a
  function in `DEVICES`; `printer-network` is `printer` plus a badge.
- To add a device, add a function and run `tools/color/build.py`.

## App icons

Phase 4 redrew the icons of the desktop's own apps, Settings
(`io.github.hblanqueto.malaysia.settings`) and Screenshot
(`io.github.hblanqueto.malaysia.screenshot`). They live in `scalable/apps`, which is
searched before `hicolor`, so they replace the copies the desktop installs in `hicolor`
whenever the Malaysia theme is active. `tools/color/build.py` generates them too; add a
row to `APPS` for a new app.

Each icon has three layers that change with the variant:

1. **Background**: a continuous-corner squircle (superellipse, n = 5) filling 824 of
   1024 units, with a two-tone vertical gradient.
2. **Figure**: the app's 16 px symbol at 3.2× with a 1.6 stroke and a short drop below.
   White in light, the app's color in dark, the accent in tinted.
3. **Edge**: an inner highlight along the top and an 18 % outline.

The shadow around the icon is left to whatever draws it (the Dock), not baked in.

The generator checks WCAG 2.2 non-text contrast (1.4.11, 3:1) between every figure and
background color and stops if a light or dark icon falls short. In the tinted variant the
accent is the user's choice, so it lightens the figure until it reaches 3:1.

## Build and install

```sh
meson setup _build
meson install -C _build
```

This installs `Malaysia` and `Malaysia-Dark` to `$prefix/share/icons/` and refreshes their
icon caches.
To use it in the Malaysia desktop, set `MALAYSIA_ICON_THEME=Malaysia` for the launcher
and choose `Malaysia` as the GTK icon theme.

## Checks

`.github/workflows/check.yml` runs on every push to `master` and on pull requests:

1. `python3 tools/symbols/export.py --check`
2. `python3 tools/color/build.py --check`
3. `python3 tools/build-icon-map.py`, then `docs/icon-map.html` must be unchanged.
4. `meson install` to a temporary prefix; both themes must get an icon cache and the
   `folder-open` link.

Run the same steps locally before pushing.

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
The desktop symbols in `src/malaysia-symbolic` also come under the MIT License of
malaysia and barrierkit (`COPYING_MIT`).
