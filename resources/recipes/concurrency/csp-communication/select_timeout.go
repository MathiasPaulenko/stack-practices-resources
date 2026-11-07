// Run: go run select_timeout.go
// Select: multiplex two inputs, exit on timeout, and cancel via context.
package main

import (
	"context"
	"fmt"
	"time"
)

// multiplex merges two channels into one until ctx is cancelled or both close.
func multiplex(ctx context.Context, ch1, ch2 <-chan string) <-chan string {
	out := make(chan string)
	go func() {
		defer close(out)
		for {
			select {
			case msg, ok := <-ch1:
				if !ok {
					ch1 = nil // disable this case forever
					continue
				}
				out <- "ch1: " + msg
			case msg, ok := <-ch2:
				if !ok {
					ch2 = nil
					continue
				}
				out <- "ch2: " + msg
			case <-ctx.Done():
				return // clean exit on cancellation — no goroutine leak
			case <-time.After(5 * time.Second):
				out <- "timeout"
				return
			}
			if ch1 == nil && ch2 == nil {
				return // both inputs closed
			}
		}
	}()
	return out
}

func ticker(name string, every time.Duration) <-chan string {
	out := make(chan string)
	go func() {
		defer close(out)
		for i := 1; i <= 3; i++ {
			time.Sleep(every)
			out <- fmt.Sprintf("%s #%d", name, i)
		}
	}()
	return out
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	for msg := range multiplex(ctx, ticker("a", 700*time.Millisecond), ticker("b", 900*time.Millisecond)) {
		fmt.Println(msg)
	}
}
