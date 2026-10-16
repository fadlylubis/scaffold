// Package job holds the work done by one cron run.
package job

import (
	"context"
	"fmt"
	"log/slog"
)

// Run processes all items and returns how many were handled.
func Run(ctx context.Context, dryRun bool) (int, error) {
	items := []string{"a", "b", "c"} // replace with real work
	for i, item := range items {
		if err := ctx.Err(); err != nil {
			return i, fmt.Errorf("stopped at %q: %w", item, err)
		}
		slog.Info("processing", "item", item, "dry_run", dryRun)
	}
	return len(items), nil
}
