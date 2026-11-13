package main

import (
	"context"
	"fmt"
	"time"
)

func workerWithCtx(ctx context.Context, id int) error {
	for {
		select {
		case <-ctx.Done():
			fmt.Printf("Worker %d cancelled: %v\n", id, ctx.Err())
			return ctx.Err()
		default:
			// Simulate work
			time.Sleep(500 * time.Millisecond)
			fmt.Printf("Worker %d working...\n", id)
		}
	}
}

func main() {
	// Timeout context: cancels after 2 seconds
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Start 3 workers
	done := make(chan struct{})
	go func() {
		workerWithCtx(ctx, 1)
		workerWithCtx(ctx, 2)
		workerWithCtx(ctx, 3)
		close(done)
	}()

	select {
	case <-done:
		fmt.Println("All workers done")
	case <-ctx.Done():
		fmt.Println("Context cancelled:", ctx.Err())
	}
}
