// Command __PROJECT__ runs a pipeline of dependent steps on an interval.
package main

import (
	"context"
	"flag"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	"__MODULE__/internal/orchestrator"
)

func main() {
	every := flag.Duration("every", time.Minute, "interval between runs; 0 runs once")
	flag.Parse()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	p, err := orchestrator.New(
		orchestrator.Step{Name: "extract", Run: logStep("extract")},
		orchestrator.Step{Name: "transform", After: []string{"extract"}, Run: logStep("transform")},
		orchestrator.Step{Name: "validate", After: []string{"extract"}, Run: logStep("validate")},
		orchestrator.Step{Name: "load", After: []string{"transform", "validate"}, Run: logStep("load")},
	)
	if err != nil {
		slog.Error("invalid pipeline", "err", err)
		os.Exit(1)
	}

	for {
		if err := p.Run(ctx); err != nil {
			slog.Error("run failed", "err", err)
			if *every == 0 {
				os.Exit(1)
			}
		}
		if *every == 0 {
			return
		}
		select {
		case <-ctx.Done():
			return
		case <-time.After(*every):
		}
	}
}

func logStep(name string) func(context.Context) error {
	return func(ctx context.Context) error {
		slog.InfoContext(ctx, "step", "name", name) // replace with real work
		return nil
	}
}
