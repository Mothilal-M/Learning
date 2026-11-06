package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// refillTokens adds one token per interval without exceeding the bucket capacity.
// It exits when ctx is cancelled.
func refillTokens(ctx context.Context, interval time.Duration, tokens chan<- struct{}) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			select {
			case tokens <- struct{}{}:
			default: // The bucket is already full; discard this tick.
			}
		}
	}
}

// newTokenBucket creates a bucket that starts full, allowing an initial burst.
func newTokenBucket(capacity int) chan struct{} {
	tokens := make(chan struct{}, capacity)
	for i := 0; i < capacity; i++ {
		tokens <- struct{}{}
	}
	return tokens
}

// Tiny token-bucket demo: allow a burst of 3 requests, then refill at ~3/sec.
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	tokens := newTokenBucket(3)

	var refill sync.WaitGroup
	refill.Add(1)
	go func() {
		defer refill.Done()
		refillTokens(ctx, 333*time.Millisecond, tokens)
	}()

	// Simulate 10 requests and show when they're allowed.
	for i := 1; i <= 10; i++ {
		<-tokens // Block until a token is available.
		fmt.Printf("allowed request %d at %s\n", i, time.Now().Format(time.RFC3339Nano))
	}

	cancel()
	refill.Wait() // Ensure the refill goroutine has exited before main returns.
}
