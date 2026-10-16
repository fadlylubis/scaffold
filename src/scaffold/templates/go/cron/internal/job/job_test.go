package job

import (
	"context"
	"errors"
	"testing"
)

func TestRun(t *testing.T) {
	if n, err := Run(context.Background(), true); err != nil || n != 3 {
		t.Fatalf("Run = %d, %v", n, err)
	}
}

func TestRunCancelled(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if _, err := Run(ctx, true); !errors.Is(err, context.Canceled) {
		t.Fatalf("err = %v, want context.Canceled", err)
	}
}
