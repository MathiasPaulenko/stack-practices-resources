package main

import (
	"fmt"
	"time"
)

func rateLimitedWorker(id int, rate <-chan time.Time) {
	for t := range rate {
		fmt.Printf("Worker %d ticked at %v\n", id, t)
		// Do rate-limited work here
	}
}

func main() {
	// 5 operations per second
	ticker := time.NewTicker(200 * time.Millisecond)
	defer ticker.Stop()

	// Run for 2 seconds
	timeout := time.After(2 * time.Second)

	go rateLimitedWorker(1, ticker.C)

	select {
	case <-timeout:
		fmt.Println("Time's up!")
	}
}
