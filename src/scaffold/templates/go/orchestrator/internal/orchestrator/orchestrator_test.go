package orchestrator

import (
	"context"
	"errors"
	"sync"
	"testing"
)

func TestRunOrderAndSkip(t *testing.T) {
	var mu sync.Mutex
	var order []string
	rec := func(name string, err error) func(context.Context) error {
		return func(context.Context) error {
			mu.Lock()
			order = append(order, name)
			mu.Unlock()
			return err
		}
	}
	boom := errors.New("boom")
	p, err := New(
		Step{Name: "a", Run: rec("a", nil)},
		Step{Name: "b", After: []string{"a"}, Run: rec("b", boom)},
		Step{Name: "c", After: []string{"b"}, Run: rec("c", nil)},
	)
	if err != nil {
		t.Fatal(err)
	}
	err = p.Run(context.Background())
	if !errors.Is(err, boom) || !errors.Is(err, ErrSkipped) {
		t.Fatalf("err = %v, want boom and skipped", err)
	}
	if len(order) != 2 || order[0] != "a" || order[1] != "b" {
		t.Fatalf("order = %v, want [a b]", order)
	}
}

func TestNewRejectsBadGraphs(t *testing.T) {
	noop := func(context.Context) error { return nil }
	cases := map[string][]Step{
		"cycle":   {{Name: "a", After: []string{"b"}, Run: noop}, {Name: "b", After: []string{"a"}, Run: noop}},
		"unknown": {{Name: "a", After: []string{"x"}, Run: noop}},
		"dup":     {{Name: "a", Run: noop}, {Name: "a", Run: noop}},
		"no run":  {{Name: "a"}},
	}
	for name, steps := range cases {
		if _, err := New(steps...); err == nil {
			t.Errorf("%s: expected error", name)
		}
	}
}
