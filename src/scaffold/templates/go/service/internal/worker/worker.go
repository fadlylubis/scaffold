// Package worker runs a unit of work on a fixed interval until cancelled.
package worker

import (
	"context"
	"log/slog"
	"time"
)

// Worker processes work every Interval.
type Worker struct {
	Interval time.Duration
	ticks    int
}

// New returns a Worker that ticks every interval.
func New(interval time.Duration) *Worker {
	return &Worker{Interval: interval}
}

// Run blocks until ctx is cancelled. Errors from a single tick are logged, not fatal.
func (w *Worker) Run(ctx context.Context) error {
	t := time.NewTicker(w.Interval)
	defer t.Stop()
	for {
		select {
		case <-ctx.Done():
			return nil
		case <-t.C:
			if err := w.process(ctx); err != nil {
				slog.Error("tick failed", "err", err)
			}
		}
	}
}

func (w *Worker) process(ctx context.Context) error {
	w.ticks++
	slog.InfoContext(ctx, "tick", "n", w.ticks) // replace with real work
	return nil
}
