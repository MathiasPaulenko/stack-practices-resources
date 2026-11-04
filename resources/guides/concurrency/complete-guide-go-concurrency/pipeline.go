// pipeline.go — stage pattern with context cancellation
package main

import "context"

func stage(ctx context.Context, in <-chan int, fn func(int) int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			select {
			case <-ctx.Done():
				return
			case out <- fn(n):
			}
		}
	}()
	return out
}
