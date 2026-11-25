// Retry budget: a token bucket that caps how much retry traffic
// your clients can generate per second. When retries share
// fate with normal traffic, an outage plus unlimited retries
// becomes a self-inflicted DDoS.
package main

import (
	"errors"
	"fmt"
	"sync"
	"syscall"
	"time"
)

type RetryBudget struct {
	mu         sync.Mutex
	tokens     float64
	maxTokens  float64
	refillRate float64 // tokens per second
	lastRefill time.Time
}

func NewRetryBudget(maxTokens, refillRate float64) *RetryBudget {
	return &RetryBudget{
		tokens:     maxTokens,
		maxTokens:  maxTokens,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
}

func (b *RetryBudget) TryAcquire() bool {
	b.mu.Lock()
	defer b.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(b.lastRefill).Seconds()
	b.tokens = min(b.maxTokens, b.tokens+elapsed*b.refillRate)
	b.lastRefill = now

	if b.tokens >= 1.0 {
		b.tokens -= 1.0
		return true
	}
	return false
}

func isRetryable(err error) bool {
	return errors.Is(err, syscall.ECONNRESET) || errors.Is(err, syscall.ETIMEDOUT)
}

func backoff(attempt int) time.Duration {
	return time.Duration(1<<attempt) * time.Second
}

// Demo: the budget allows a burst, then throttles retries to refillRate.
func main() {
	budget := NewRetryBudget(10, 2) // burst of 10, then 2 retries/sec
	allowed := 0
	for i := 0; i < 20; i++ {
		if budget.TryAcquire() {
			allowed++
		}
	}
	fmt.Printf("20 retry attempts, %d allowed by budget\n", allowed)
}
