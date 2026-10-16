// Command __PROJECT__ runs a long-lived background service.
package main

import (
	"context"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	"__MODULE__/internal/worker"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	w := worker.New(5 * time.Second)
	if err := w.Run(ctx); err != nil {
		slog.Error("exit", "err", err)
		os.Exit(1)
	}
	slog.Info("stopped")
}
