// Package orchestrator runs steps as a DAG: each step starts once all steps it
// depends on have succeeded. Independent steps run concurrently.
package orchestrator

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"time"
)

// Step is one unit of work. After lists the names of steps that must succeed first.
type Step struct {
	Name  string
	After []string
	Run   func(context.Context) error
}

// ErrSkipped marks a step that did not run because a dependency failed.
var ErrSkipped = errors.New("skipped: dependency failed")

// Pipeline is a validated set of steps.
type Pipeline struct {
	steps []Step
}

// New validates names, dependencies and acyclicity.
func New(steps ...Step) (*Pipeline, error) {
	byName := make(map[string]Step, len(steps))
	for _, s := range steps {
		if s.Name == "" || s.Run == nil {
			return nil, fmt.Errorf("step %q: name and Run are required", s.Name)
		}
		if _, dup := byName[s.Name]; dup {
			return nil, fmt.Errorf("duplicate step %q", s.Name)
		}
		byName[s.Name] = s
	}
	const (
		visiting = 1
		done     = 2
	)
	state := make(map[string]int, len(steps))
	var visit func(string) error
	visit = func(name string) error {
		switch state[name] {
		case visiting:
			return fmt.Errorf("cycle at step %q", name)
		case done:
			return nil
		}
		state[name] = visiting
		for _, dep := range byName[name].After {
			if _, ok := byName[dep]; !ok {
				return fmt.Errorf("step %q depends on unknown step %q", name, dep)
			}
			if err := visit(dep); err != nil {
				return err
			}
		}
		state[name] = done
		return nil
	}
	for _, s := range steps {
		if err := visit(s.Name); err != nil {
			return nil, err
		}
	}
	return &Pipeline{steps: steps}, nil
}

// Run executes every step and returns all step errors joined.
func (p *Pipeline) Run(ctx context.Context) error {
	// Slices, not maps: each goroutine writes only its own index, and readers
	// wait on done[i] before reading errs[i].
	idx := make(map[string]int, len(p.steps))
	done := make([]chan struct{}, len(p.steps))
	errs := make([]error, len(p.steps))
	for i, s := range p.steps {
		idx[s.Name] = i
		done[i] = make(chan struct{})
	}
	for i, s := range p.steps {
		go func() {
			defer close(done[i])
			for _, dep := range s.After {
				<-done[idx[dep]]
				if errs[idx[dep]] != nil {
					errs[i] = ErrSkipped
					return
				}
			}
			start := time.Now()
			if err := s.Run(ctx); err != nil {
				errs[i] = err
				slog.Error("step failed", "step", s.Name, "err", err)
				return
			}
			slog.Info("step ok", "step", s.Name, "elapsed", time.Since(start))
		}()
	}
	var all []error
	for i, s := range p.steps {
		<-done[i]
		if errs[i] != nil {
			all = append(all, fmt.Errorf("%s: %w", s.Name, errs[i]))
		}
	}
	return errors.Join(all...)
}
