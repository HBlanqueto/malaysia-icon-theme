#!/usr/bin/env python3
"""Copy the symbolic icons of MacTahoe-icon-theme (GPL-3) into Malaysia/symbolic, unchanged.

Usage: python3 tools/symbols/import_mactahoe.py <MacTahoe-icon-theme path>

MacTahoe installs src/<context>/<dir> and links/<context>/<dir> into one <context>/<dir>, and
where a name is in several contexts the first one in ORDER wins, as in its index.theme. Each
name gets the drawing it resolves to there: a symlink when that drawing is the one the theme
already shows under the alias's target, a copy otherwise.

A name the theme already has keeps its context; a new name takes MacTahoe's context (mimes
becomes mimetypes). The battery family stays Malaysia's own. Emotes are left to Adwaita
(AGENTS.md, rule 7). Every source in src/malaysia-symbolic that a copy replaces is removed, so
tools/symbols/export.py no longer writes it.
"""
import os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "Malaysia", "symbolic")
SRC = os.path.join(ROOT, "src", "malaysia-symbolic")
CONTEXTS = {"mimes": "mimetypes"}
ORDER = ("actions", "apps", "categories", "places", "mimes", "devices", "emblems", "status")


def ours(name):
    return name.startswith("battery")


def installed(theme, ctx, rel):
    """The file MacTahoe installs at <ctx>/symbolic/<rel>, following its aliases."""
    path = os.path.normpath(os.path.join("symbolic", rel))
    for _ in range(16):
        for kind in ("src", "links"):
            candidate = os.path.join(theme, kind, ctx, path)
            if os.path.islink(candidate):
                path = os.path.normpath(os.path.join(os.path.dirname(path), os.readlink(candidate)))
                break
            if os.path.isfile(candidate):
                return candidate, path
        else:
            return None, None
    return None, None


def winners(theme):
    seen = {}
    for ctx in ORDER:
        for kind in ("src", "links"):
            folder = os.path.join(theme, kind, ctx, "symbolic")
            for f in sorted(os.listdir(folder)) if os.path.isdir(folder) else ():
                if f.endswith(".svg") and not ours(f) and f not in seen:
                    seen[f] = ctx
    return seen


def place(ctx, f, where):
    target = where.get(f, CONTEXTS.get(ctx, ctx))
    dest = os.path.join(OUT, target, f)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.lexists(dest):
        os.remove(dest)
    source = os.path.join(SRC, target, f)
    if os.path.exists(source):
        os.remove(source)
    where[f] = target
    return dest


def main(theme):
    where = {f: ctx for ctx in os.listdir(OUT) for f in os.listdir(os.path.join(OUT, ctx))}
    names = winners(theme)
    drawing = {f: installed(theme, ctx, f) for f, ctx in names.items()}
    own = {f: path for f, (path, rel) in drawing.items() if path and rel == os.path.join("symbolic", f)}
    copied = linked = 0
    for f in own:
        shutil.copyfile(own[f], place(names[f], f, where))
        copied += 1
    for f, (path, rel) in drawing.items():
        if f in own or not path:
            continue
        target = os.path.basename(rel)
        dest = place(names[f], f, where)
        if own.get(target) == path:
            here = where[f]
            os.symlink(target if where[target] == here else f"../{where[target]}/{target}", dest)
            linked += 1
        else:
            shutil.copyfile(path, dest)
            copied += 1
    print(f"{copied} icons and {linked} aliases from MacTahoe in Malaysia/symbolic")


if __name__ == "__main__":
    main(sys.argv[1])
