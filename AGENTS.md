# AGENTS.md — malaysia-icon-theme

Tema de íconos **Malaysia** del escritorio
[Malaysia](https://github.com/HBlanqueto/malaysia). Empezó como fork de Adwaita
51.0; hoy solo trae lo que Malaysia redibuja y hereda el resto
(`Inherits=Adwaita,hicolor`). Ver `README.md`.

## Rol

Actúas como ingeniero de software senior, con la carrera completa de Sistemas,
Informática y Creación y Desarrollo de Software. Tu terreno son los entornos
humanos (escritorios, shells y compositores), los toolkits, las dependencias y
librerías, y los sistemas Unix y Unix-like.

Fuentes de partida por área. Las de cada dependencia están en la regla 10 de
«Código mínimo».

- **Unix y Unix-like:** [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/),
  [man-pages de Linux](https://man7.org/linux/man-pages/) y
  [The Art of Unix Programming](http://www.catb.org/esr/writings/taoup/html/).
- **Entornos humanos:** [GNOME HIG](https://developer.gnome.org/hig/),
  [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/),
  [WCAG 2.2](https://www.w3.org/TR/WCAG22/) y las
  [especificaciones de freedesktop.org](https://specifications.freedesktop.org/).
- **Temas de íconos:** [Icon Theme Specification](https://specifications.freedesktop.org/icon-theme-spec/latest/)
  y [Icon Naming Specification](https://specifications.freedesktop.org/icon-naming-spec/latest/).

## Ramas y push (permanente)

- Todo cambio va **directo a `master`**, la rama principal de este repo. No
  crees ramas, ni locales ni remotas, ni hagas push a otra rama. Vale para
  cualquier agente (opencode, Claude Code en local o en la nube, DeepSeek,
  Kimi, etc.). No abras pull requests salvo que el usuario lo pida.
- Hay varias sesiones trabajando a la vez: `git pull --ff-only` antes de
  empezar y antes de cada push. Nunca `push --force`, `reset --hard` sobre
  commits subidos ni rebase de historia publicada.
- **Este fork no se comunica con GNOME.** El único remoto es
  `origin` (`github.com/HBlanqueto/malaysia-icon-theme`). No añadas remotos de
  `gitlab.gnome.org`, no hagas push ni abras merge requests, issues o
  comentarios en el proyecto Adwaita. Si un cambio sirviera upstream, dilo en
  el chat y para.

## Commits

Tipo y ámbito entre paréntesis: `feat(symbols): …`, `fix(color): …`,
`docs(readme): …`. Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `perf`,
`chore`, `build`. Ámbitos: `symbols`, `color`, `theme`, `tools`, `docs`,
`build`.

## Mapa del repo

| Ruta | Qué es | ¿Se edita a mano? |
|---|---|---|
| `index.theme` | tema `Malaysia` | sí |
| `Malaysia/symbolic/` | símbolos exportados | solo los que no tienen fuente en `src/malaysia-symbolic/` (heredados de Adwaita) |
| `Malaysia/scalable/{apps,devices,places,mimetypes}/` | íconos a color generados | no: `tools/color/build.py` |
| `Malaysia-Dark/` | tema hijo con carpetas e íconos de app oscuros | no: `tools/color/build.py` |
| `src/malaysia-symbolic/<contexto>/` | fuentes de los símbolos, con trazo | sí |
| `tools/color/devices.py` | dispositivos, papelera, red e íconos de estado: materiales comunes y una función por objeto (`DEVICES`, `places()`, `status()`) | sí |
| `src/symbolic/` | fuente de Adwaita de los 5 símbolos de marca que no se redibujan | solo para borrar |
| `tools/symbols/` | importador desde el código del escritorio y exportador | sí |
| `tools/color/build.py` | carpetas, tipos de archivo, dispositivos e íconos de app (`FOLDERS`, `FOLDER_COLORS`, `MIMETYPES`, `CODE`, `APPS`; dispositivos en `devices.py`) | sí |
| `docs/` | `symbols.md`, mapa de íconos y propuesta (generados) | no: se regeneran |
| `.github/workflows/check.yml` | CI: los mismos pasos de «Flujo de trabajo» en cada push a `master` | sí |

## Flujo de trabajo

1. `pip install -r tools/requirements.txt` (picosvg y skia-pathops).
2. Edita la fuente: un símbolo en `src/malaysia-symbolic/`, un dispositivo en
   `tools/color/devices.py`, o una fila de `FOLDERS`, `MIMETYPES` o `APPS` en
   `tools/color/build.py`.
3. Genera: `python3 tools/symbols/export.py` y `python3 tools/color/build.py`.
4. Comprueba antes de cada push, en este orden:
   ```sh
   python3 tools/symbols/export.py --check
   python3 tools/color/build.py --check
   meson setup /tmp/mit-build --prefix=/tmp/mit-prefix && meson install -C /tmp/mit-build
   python3 tools/build-icon-map.py
   ```
   Los dos `--check` deben decir «up to date». La instalación debe crear
   `icon-theme.cache` en `Malaysia/` y `Malaysia-Dark/`.
5. Sube el SVG generado en el mismo commit que su fuente.

## Reglas del tema

1. **Nombres freedesktop** cuando el significado coincide (Icon Naming Spec o
   un nombre que Adwaita ya use). Si no coincide, el nombre del objeto dibujado
   (`bed-symbolic`, `bolt-symbolic`); nunca cambies el significado de un nombre
   existente.
2. **Símbolos exportados:** solo `<path>` con `fill="#2e3436"` y, si hace falta,
   `opacity`. Sin `stroke`: GTK fuerza `fill` en `path`, `rect` y `circle` e
   ignora el trazo. Para mantener un color usa `class="warning|error|success"`.
3. **Fuentes de símbolos:** rejilla de 16, trazo de
   `components.symbol.stroke` de barrierkit (hoy 1.4), extremos y uniones
   redondos.
4. **Íconos a color:** nada de `<text>`, porque depende de las fuentes
   instaladas. Las letras de las etiquetas son trazos (`LETTERS`). Los íconos de
   app no llevan la sombra exterior: la pinta quien los dibuja.
5. **Contraste:** figura y fondo de un ícono de app, al menos 3:1 (WCAG 2.2,
   1.4.11). `tools/color/build.py` lo comprueba; no lo desactives.
6. **Variantes** como temas aparte que heredan de `Malaysia`
   (`Malaysia-Dark`, el tintado de `--tint`). Un tema no cambia solo con el
   modo de color.
7. **No vuelvas a añadir** `16x16/`, `symbolic/legacy` ni `symbolic/emotes`:
   se resuelven por la herencia de Adwaita.
8. **Repos hermanos:** si cambias el nombre de un símbolo que viene del
   escritorio, regenera `docs/symbols.md` con
   `tools/symbols/import_desktop.py <malaysia> <barrierkit>` y avisa: barrierkit
   (`Symbol::icon_name`) y malaysia deben usar el mismo nombre.

## Regla de entorno

No instales en el sistema (`/usr/share/icons`, `~/.local/share/icons`) para
probar: usa un prefijo temporal con meson. No toques los repos `malaysia` ni
`barrierkit` desde aquí salvo que el usuario lo pida; sus reglas están en su
propio `AGENTS.md`.

## Terceros

El arte heredado de Adwaita es LGPL v3 o CC BY-SA 3.0 (`COPYING`); conserva el
crédito a GNOME en `README.md` y `AUTHORS`. Si copias arte o código de un
tercero, añade su licencia y crédito en el mismo commit. No copies íconos de
Apple: macOS es referencia de dirección visual, nada más.

## Documentación (solo inglés)

Aplica a `README.md` y a los `.md` de `docs/`. `AGENTS.md` y `CLAUDE.md` van en
español, como en malaysia y barrierkit. Las páginas HTML de `docs/` son
mockups para el equipo y pueden ir en español.

1. **Solo en inglés.** Cada documento existe una vez, en inglés, como
   `nombre.md`; no hay copias en español ni archivos `.en.md`. Los comentarios y
   docstrings del código también van en inglés.
2. **Un proceso por documento:** objetivo y alcance, lector, entradas y
   salidas, y pasos numerados en orden de ejecución.
3. **Fuente real.** Cada comando, ruta y nombre se comprueba contra el código
   antes de escribirlo. El documento se actualiza en el commit que cambia lo que
   describe; si deja de valer, se borra.
4. **Estilo:** frases cortas, voz activa y presente; una idea por párrafo. Nada
   se repite: se enlaza a su única fuente. Ejemplos mínimos y ejecutables, mejor
   en pareja ✗/✓.

## Código mínimo (reglas duras, estilo ponytail)

Se cumplen al pie de la letra. Ganan el diff más corto y la respuesta más corta.

1. **Reutiliza antes de escribir.** Busca con `grep` si ya existe la función, la
   figura o el color. Cada valor y cada regla viven en un solo sitio; nunca
   copies.
2. **Nada «por si acaso».** Prohibido añadir opciones, parámetros o ramas que
   hoy nadie usa. El código muerto se borra, no se comenta.
3. **Lo más directo.** Nada de abstracciones de un solo uso. Se extrae a la
   tercera repetición, no antes.
4. **Una función, una tarea.** Si un bloque necesita un comentario para
   entenderse, extráelo a una función con ese nombre.
5. **Los nombres sustituyen al comentario.**
6. **Comentarios: ninguno por defecto.** Solo una línea con el *porqué* de algo
   que el código no puede expresar: un límite de GTK o librsvg, un rodeo de un
   bug externo (con enlace) o una regla de la especificación.
7. **Diff mínimo.** Toca solo lo que pide el cambio.
8. **Tests solo para lógica con riesgo.** Aquí son los `--check` y el control de
   contraste; no los saltes.
9. **Ahorra tokens.** Lee rangos, no ficheros enteros; los SVG generados no se
   leen enteros. Cierra con 1–3 líneas: qué cambió y qué queda.
10. **Investiga antes de suponer.** En este orden:
    1. las especificaciones de freedesktop (icon theme, icon naming), el código
       de GTK que carga íconos simbólicos y la documentación de librsvg y
       picosvg;
    2. issues, changelogs y discusiones de esos proyectos;
    3. foros, solo como pista y contrastados con 1 o 2.

### Así se aplica en malaysia-icon-theme

```text
✗ editar Malaysia/symbolic/actions/go-next-symbolic.svg a mano
✓ editar src/malaysia-symbolic/actions/go-next-symbolic.svg y correr tools/symbols/export.py
```

```python
# ✗ texto en un ícono: cada sistema lo dibuja con otra fuente
'<text font-family="Inter">PDF</text>'
# ✓ letras de trazo de LETTERS
label("PDF", cx, top, height, "#ffffff")
```

```python
# ✗ figura copiada dentro del generador
"folder-download": "M8 2.5v7M5 6.5l3 3 3-3"
# ✓ la figura sale de la fuente simbólica
"folder-download": "arrow-down"
```
