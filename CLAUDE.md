# CLAUDE.md

@AGENTS.md

## Regla de ramas (prioridad máxima)

Todo commit va **directo a `master`** y se sube con `git push origin master`.
No crees ramas (tampoco ramas `claude/...` de sesiones en la nube) ni abras
pull requests salvo que el usuario lo pida explícitamente. `git pull --ff-only`
antes de cada push; nunca `--force`.

Nada sale de este fork: el único remoto es `origin`
(`github.com/HBlanqueto/malaysia-icon-theme`). Nunca hagas push, merge requests
ni comentarios en el Adwaita de GNOME.
