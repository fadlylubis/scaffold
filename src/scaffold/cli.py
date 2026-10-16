"""scaffold: render a project from layered templates.

Template `<lang>/<kind>` = `<lang>/_base` copied first, then `<lang>/<kind>` on top.
Tokens in paths and file contents: __PROJECT__, __PACKAGE__, __MODULE__.
Path parts starting with `dot-` become `.` (keeps template .gitignore files inert in this repo).
Plain tokens instead of Jinja because Vue and Go templates already use {{ }}.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

TEMPLATES = Path(__file__).parent / "templates"
NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def available() -> list[str]:
    return sorted(
        f"{lang.name}/{kind.name}"
        for lang in TEMPLATES.iterdir()
        if lang.is_dir()
        for kind in lang.iterdir()
        if kind.is_dir() and kind.name != "_base"
    )


def render(template: str, name: str, dest: Path, module: str | None = None) -> Path:
    if template not in available():
        raise ValueError(f"unknown template {template!r}; try: {', '.join(available())}")
    if not NAME_RE.match(name):
        raise ValueError(f"invalid name {name!r}: use lowercase letters, digits and dashes")
    target = dest / name
    if target.exists():
        raise FileExistsError(f"{target} already exists")

    tokens = {
        "__PROJECT__": name,
        "__PACKAGE__": name.replace("-", "_"),
        "__MODULE__": module or name,
    }
    lang = template.split("/")[0]
    layers = [TEMPLATES / lang / "_base", TEMPLATES / template]
    for layer in (l for l in layers if l.is_dir()):
        for src in sorted(layer.rglob("*")):
            if src.is_dir() or "__pycache__" in src.parts or src.name == ".DS_Store":
                continue
            rel = src.relative_to(layer).as_posix()
            for k, v in tokens.items():
                rel = rel.replace(k, v)
            rel = "/".join("." + p[4:] if p.startswith("dot-") else p for p in rel.split("/"))
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                text = src.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                shutil.copyfile(src, out)
                continue
            for k, v in tokens.items():
                text = text.replace(k, v)
            out.write_text(text, encoding="utf-8")
    return target


def ask(prompt: str, default: str = "") -> str:
    """Prompt until non-empty; Enter accepts the default."""
    while True:
        value = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip() or default
        if value:
            return value


def plan() -> tuple[str, str, Path, str | None] | None:
    """Ask cookiecutter-style questions. Returns render args, or None if declined."""
    templates = available()
    print("Templates:")
    for i, t in enumerate(templates, 1):
        print(f"  {i:>2}. {t}")
    while True:
        choice = ask("Template (number or name)", "1")
        if choice.isdigit() and 1 <= int(choice) <= len(templates):
            template = templates[int(choice) - 1]
            break
        if choice in templates:
            template = choice
            break
        print(f"  pick 1-{len(templates)} or a name from the list")
    while not NAME_RE.match(name := ask("Project name", "my-project")):
        print("  use lowercase letters, digits and dashes, starting with a letter")
    out = Path(ask("Parent directory", str(Path.cwd()))).expanduser()
    module = ask("Go module path", f"github.com/you/{name}") if template.startswith("go/") else None

    print(
        f"\n  template  {template}\n  path      {out / name}"
        + (f"\n  module    {module}" if module else "")
    )
    if ask("Create it? (y/n)", "y").lower() not in ("y", "yes"):
        return None
    return template, name, out, module


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="scaffold", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list templates")
    sub.add_parser("plan", help="answer questions, then create a project")
    new = sub.add_parser("new", help="create a project")
    new.add_argument("template", help="e.g. python/fastapi, go/api, vue/app")
    new.add_argument("name", help="project name (lowercase, dashes)")
    new.add_argument("-o", "--out", type=Path, default=Path.cwd(), help="parent directory")
    new.add_argument("-m", "--module", help="Go module path (default: name)")
    args = p.parse_args(argv)

    if args.cmd == "list":
        print("\n".join(available()))
        return 0
    if args.cmd == "plan":
        try:
            answers = plan()
        except (KeyboardInterrupt, EOFError):
            print("\ncancelled")
            return 130
        if answers is None:
            print("cancelled")
            return 1
    else:
        answers = (args.template, args.name, args.out, args.module)
    try:
        target = render(*answers)
    except (ValueError, FileExistsError) as e:
        print(f"scaffold: {e}", file=sys.stderr)
        return 1
    print(f"created {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
