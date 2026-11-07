package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// refillTokens adds one token per interval without exceeding the bucket capacity.
// It exits when ctx is cancelled and rejects invalid configuration.
func refillTokens(ctx context.Context, interval time.Duration, tokens chan<- struct{}) error {
	if ctx == nil {
		return fmt.Errorf("context must not be nil")
	}
	if interval <= 0 {
		return fmt.Errorf("refill interval must be positive")
	}
	if tokens == nil {
		return fmt.Errorf("tokens channel must not be nil")
	}

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return nil
		case <-ticker.C:
			select {
			case tokens <- struct{}{}:
			default: // The bucket is already full; discard this tick.
			}
		}
	}
}

// newTokenBucket creates a bucket that starts full, allowing an initial burst.
func newTokenBucket(capacity int) (chan struct{}, error) {
	if capacity < 1 {
		return nil, fmt.Errorf("bucket capacity must be at least 1")
	}

	tokens := make(chan struct{}, capacity)
	for i := 0; i < capacity; i++ {
		tokens <- struct{}{}
	}
	return tokens, nil
}

// Tiny token-bucket demo: allow a burst of 3 requests, then refill at ~3/sec.
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	tokens, err := newTokenBucket(3)
	if err != nil {
		panic(err)
	}

	var refill sync.WaitGroup
	refill.Add(1)
	refillErr := make(chan error, 1)
	go func() {
		defer refill.Done()
		refillErr <- refillTokens(ctx, 333*time.Millisecond, tokens)
	}()

	// Simulate 10 requests and show when they're allowed.
	for i := 1; i <= 10; i++ {
		select {
		case <-tokens: // Block until a token is available.
		case err := <-refillErr:
			if err != nil {
				panic(err)
			}
			panic("token refill stopped before all requests were allowed")
		}
		fmt.Printf("allowed request %d at %s\n", i, time.Now().Format(time.RFC3339Nano))
	}

	cancel()
	refill.Wait() // Ensure the refill goroutine has exited before main returns.
	if err := <-refillErr; err != nil {
		panic(err)
	}
}
