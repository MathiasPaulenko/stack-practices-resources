// Retry helper with exponential backoff and jitter (standard library only).
// Companion code for https://stackpractices.com/recipes/retry-logic-exponential-backoff/
package main

import (
	"context"
	"fmt"
	"math"
	"math/rand"
	"time"
)

func withRetry(ctx context.Context, fn func() error, maxRetries int, baseDelay time.Duration) error {
	for attempt := 0; attempt <= maxRetries; attempt++ {
		err := fn()
		if err == nil {
			return nil
		}
		if attempt == maxRetries {
			return fmt.Errorf("after %d retries: %w", maxRetries, err)
		}

		delay := float64(baseDelay) * math.Pow(2, float64(attempt))
		jitter := rand.Float64() * delay * 0.5
		select {
		case <-time.After(time.Duration(delay + jitter)):
		case <-ctx.Done():
			return ctx.Err()
		}
	}
	return nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	err := withRetry(ctx, func() error {
		// simulates a call that fails
		return nil
	}, 5, time.Second)
	fmt.Println("Result:", err)
}
