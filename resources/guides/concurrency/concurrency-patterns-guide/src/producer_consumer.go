// Producer-consumer in Go: a buffered channel is the bounded queue,
// close(jobs) is the shutdown signal, WaitGroup waits for workers.
// Run: go run producer_consumer.go
// Race check: go run -race producer_consumer.go
package main

import (
	"fmt"
	"sync"
	"time"
)

func process(job int) {
	time.Sleep(5 * time.Millisecond)
	fmt.Printf("  processed job %d\n", job)
}

func main() {
	jobs := make(chan int, 10) // buffered channel = bounded queue
	var wg sync.WaitGroup

	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for job := range jobs { // exits when channel is closed and drained
				fmt.Printf("worker %d: ", id)
				process(job)
			}
		}(w)
	}

	for i := 0; i < 20; i++ {
		jobs <- i // blocks when the buffer is full — backpressure
	}
	close(jobs)
	wg.Wait()
	fmt.Println("all work drained")
}
