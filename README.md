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

## Build and install

```sh
meson setup _build
meson install -C _build
```

This installs the theme to `$prefix/share/icons/Malaysia` and refreshes its icon cache.
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
