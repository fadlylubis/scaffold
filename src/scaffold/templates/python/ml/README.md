# __PROJECT__

```sh
uv sync
uv run train            # writes models/model.joblib
uv run jupyter lab      # notebooks/ for exploration
make test
```

`data/` and `models/` are git-ignored.

Git hooks (gitleaks, lint, hygiene), run once:

```sh
make hooks
```
