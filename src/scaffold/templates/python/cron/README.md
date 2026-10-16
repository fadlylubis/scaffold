# __PROJECT__

```sh
uv sync
uv run __PROJECT__ --dry-run
make test
```

Crontab example:

```
0 * * * * cd /path/to/__PROJECT__ && uv run --no-dev __PROJECT__ >> /var/log/__PROJECT__.log 2>&1
```

Git hooks (gitleaks, lint, hygiene), run once:

```sh
make hooks
```
