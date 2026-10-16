# scaffold

Personal project scaffolding, like cookiecutter but with no prompts and no Jinja.

```sh
uv tool install -e .          # puts `scaffold` on PATH
scaffold plan                 # asks questions, like cookiecutter
scaffold list
scaffold new python/fastapi my-api
scaffold new go/api my-svc -m github.com/me/my-svc
scaffold new vue/app my-ui -o ~/Development
```

## Templates

| Template | What you get |
|---|---|
| `python/lib` | uv package, src layout, pytest, ruff |
| `python/fastapi` | FastAPI service, router, tests, Dockerfile |
| `python/streamlit` | Streamlit app with theme config and an AppTest smoke test |
| `python/notebook` | JupyterLab, pandas, matplotlib, git-ignored `data/` |
| `python/ml` | scikit-learn train script, `models/`, `data/`, notebooks |
| `python/cron` | One-shot job with CLI entry point, logging, exit codes |
| `go/api` | net/http with method routing, graceful shutdown, table tests |
| `go/service` | Long-running ticker worker with graceful shutdown |
| `go/cron` | One-shot job with timeout and signal handling |
| `go/orchestrator` | DAG of steps run concurrently, cycle checks, interval loop |
| `vue/app` | Vue 3 + Vite + TS, design tokens, app shell, light and dark theme |

## Git hooks

Every template ships a pre-commit config that runs gitleaks, basic file checks, and the language linter: ruff for Python, gofmt and go vet for Go.
Inside a new project, run `make hooks`, or `npm run hooks` for Vue.
It runs `git init` and installs the hooks through `uvx pre-commit`, so nothing extra needs installing.
This repo uses the same hooks: `uvx pre-commit install`.

## Adding a template

Templates live in `src/scaffold/templates/<lang>/<kind>/`.
Files in `<lang>/_base/` are copied first, then `<kind>/` overwrites them.

Tokens replaced in file names and contents:

- `__PROJECT__` is the name as typed (`my-api`).
- `__PACKAGE__` is the Python package name (`my_api`).
- `__MODULE__` is the Go module path (`-m`, defaults to the name).

Name a file `dot-gitignore` to get `.gitignore`. This keeps template ignore rules from affecting this repo.

```sh
uv run pytest
```
