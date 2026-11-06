package main

import (
	"context"
	"testing"
	"time"
)

func TestNewTokenBucketStartsFull(t *testing.T) {
	tokens := newTokenBucket(3)
	if got := len(tokens); got != 3 {
		t.Fatalf("new bucket contains %d tokens; want 3", got)
	}
	if got := cap(tokens); got != 3 {
		t.Fatalf("new bucket capacity is %d; want 3", got)
	}
}

func TestRefillTokensDoesNotExceedCapacity(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	tokens := make(chan struct{}, 1)
	tokens <- struct{}{} // Begin with a full bucket.
	done := make(chan struct{})

	go func() {
		refillTokens(ctx, time.Millisecond, tokens)
		close(done)
	}()

	time.Sleep(15 * time.Millisecond)
	if got := len(tokens); got != 1 {
		t.Fatalf("bucket contains %d tokens; want capacity 1", got)
	}

	cancel()
	select {
	case <-done:
	case <-time.After(time.Second):
		t.Fatal("refill goroutine did not stop after cancellation")
	}
}

func TestRefillTokensStopsOnCancellation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	tokens := make(chan struct{}, 1)
	done := make(chan struct{})

	go func() {
		refillTokens(ctx, time.Hour, tokens)
		close(done)
	}()

	cancel()
	select {
	case <-done:
	case <-time.After(time.Second):
		t.Fatal("refill goroutine did not stop after cancellation")
	}
}
