# __PROJECT__

Go service. Layout: `cmd/__PROJECT__` is the entry point, `internal/` holds the code.

```sh
make run
make test
make lint
docker build -t __PROJECT__ .
```

Git hooks (gitleaks, lint, hygiene), run once:

```sh
make hooks
```
