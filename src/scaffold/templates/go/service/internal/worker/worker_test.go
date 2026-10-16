package worker

import (
	"context"
	"testing"
	"time"
)

func TestRunStopsOnCancel(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 35*time.Millisecond)
	defer cancel()
	w := New(10 * time.Millisecond)
	if err := w.Run(ctx); err != nil {
		t.Fatal(err)
	}
	if w.ticks == 0 {
		t.Error("expected at least one tick")
	}
}
