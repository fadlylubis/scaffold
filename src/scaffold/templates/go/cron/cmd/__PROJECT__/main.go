// Command __PROJECT__ runs one job and exits. Non-zero exit means failure.
package main

import (
	"context"
	"flag"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	"__MODULE__/internal/job"
)

func main() {
	timeout := flag.Duration("timeout", 10*time.Minute, "max run time")
	dryRun := flag.Bool("dry-run", false, "log actions without side effects")
	flag.Parse()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	ctx, cancel := context.WithTimeout(ctx, *timeout)
	defer cancel()

	start := time.Now()
	n, err := job.Run(ctx, *dryRun)
	if err != nil {
		slog.Error("job failed", "err", err)
		os.Exit(1)
	}
	slog.Info("done", "items", n, "elapsed", time.Since(start))
}
