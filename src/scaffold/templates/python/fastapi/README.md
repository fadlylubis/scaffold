# __PROJECT__

FastAPI service.

```sh
uv sync
uv run fastapi dev src/__PACKAGE__/main.py   # http://localhost:8000/docs
make test
docker build -t __PROJECT__ .
```

Git hooks (gitleaks, lint, hygiene), run once:

```sh
make hooks
```
