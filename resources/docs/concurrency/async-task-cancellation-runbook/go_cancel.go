// Async task cancellation demo for Go (context.Context).
//
// Run: go run go_cancel.go
// The context auto-cancels after 2 seconds via WithTimeout.
package main

import (
	"context"
	"fmt"
	"time"
)

func longRunningTask(ctx context.Context, taskID string) error {
	for i := 0; i < 1000; i++ {
		select {
		case <-ctx.Done():
			fmt.Printf("Task %s: cancelled, cleaning up...\n", taskID)
			cleanupResources(taskID)
			return ctx.Err()
		default:
		}

		time.Sleep(100 * time.Millisecond)
		fmt.Printf("Task %s: processing item %d\n", taskID, i)
	}
	return nil
}

func cleanupResources(taskID string) {
	fmt.Printf("Task %s: closing connections...\n", taskID)
	time.Sleep(50 * time.Millisecond)
	fmt.Printf("Task %s: cleanup complete\n", taskID)
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel() // required: releases the timer goroutine

	if err := longRunningTask(ctx, "worker-1"); err != nil {
		fmt.Printf("Task ended: %v\n", err)
	}
}
