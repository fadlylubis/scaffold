"""One-shot job meant to be run by cron/systemd/k8s CronJob. Exit code 0 = success."""

import argparse
import logging
import sys
import time

log = logging.getLogger("__PROJECT__")


def run(dry_run: bool) -> int:
    """Do the work; return the number of items processed."""
    items = ["a", "b", "c"]  # replace with real work
    for item in items:
        log.info("processing %s%s", item, " (dry run)" if dry_run else "")
    return len(items)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    start = time.monotonic()
    try:
        n = run(args.dry_run)
    except Exception:
        log.exception("job failed")
        return 1
    log.info("done items=%d elapsed=%.2fs", n, time.monotonic() - start)
    return 0


if __name__ == "__main__":
    sys.exit(main())
