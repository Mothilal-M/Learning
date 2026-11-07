package main

import (
	"context"
	"testing"
	"time"
)

func TestNewTokenBucketStartsFull(t *testing.T) {
	tokens, err := newTokenBucket(3)
	if err != nil {
		t.Fatalf("newTokenBucket returned an error: %v", err)
	}
	if got := len(tokens); got != 3 {
		t.Fatalf("new bucket contains %d tokens; want 3", got)
	}
	if got := cap(tokens); got != 3 {
		t.Fatalf("new bucket capacity is %d; want 3", got)
	}
}

func TestNewTokenBucketRejectsInvalidCapacity(t *testing.T) {
	for _, capacity := range []int{0, -1} {
		tokens, err := newTokenBucket(capacity)
		if err == nil {
			t.Errorf("newTokenBucket(%d) should return an error", capacity)
		}
		if tokens != nil {
			t.Errorf("newTokenBucket(%d) returned a channel; want nil", capacity)
		}
	}
}

func TestRefillTokensDoesNotExceedCapacity(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	tokens := make(chan struct{}, 1)
	tokens <- struct{}{} // Begin with a full bucket.
	done := make(chan struct{})

	go func() {
		if err := refillTokens(ctx, time.Millisecond, tokens); err != nil {
			t.Errorf("refillTokens returned an error: %v", err)
		}
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
	done := make(chan struct{})

	go func() {
		if err := refillTokens(ctx, time.Hour, make(chan struct{}, 1)); err != nil {
			t.Errorf("refillTokens returned an error: %v", err)
		}
		close(done)
	}()

	cancel()
	select {
	case <-done:
	case <-time.After(time.Second):
		t.Fatal("refill goroutine did not stop after cancellation")
	}
}

func TestRefillTokensRejectsInvalidConfiguration(t *testing.T) {
	validContext := context.Background()
	validTokens := make(chan struct{}, 1)

	cases := []struct {
		name     string
		ctx      context.Context
		interval time.Duration
		tokens   chan struct{}
	}{
		{name: "nil context", ctx: nil, interval: time.Second, tokens: validTokens},
		{name: "zero interval", ctx: validContext, interval: 0, tokens: validTokens},
		{name: "negative interval", ctx: validContext, interval: -time.Second, tokens: validTokens},
		{name: "nil channel", ctx: validContext, interval: time.Second, tokens: nil},
	}

	for _, testCase := range cases {
		t.Run(testCase.name, func(t *testing.T) {
			if err := refillTokens(testCase.ctx, testCase.interval, testCase.tokens); err == nil {
				t.Fatal("refillTokens should reject invalid configuration")
			}
		})
	}
}
