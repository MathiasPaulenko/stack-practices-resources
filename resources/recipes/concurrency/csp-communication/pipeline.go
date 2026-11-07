// Run: go run pipeline.go
// CSP pipeline: generator → square → print, plus fan-out/fan-in workers.
package main

import (
	"fmt"
	"sync"
	"time"
)

// generator produces the given numbers on a channel it owns and closes.
func generator(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		for _, n := range nums {
			out <- n
		}
		close(out) // sender closes — receivers see the zero value + ok=false
	}()
	return out
}

// square transforms each input until the channel is closed, then closes its own output.
func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n * n
		}
		close(out)
	}()
	return out
}

// worker consumes jobs and emits results until jobs is closed.
func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range jobs {
		fmt.Printf("worker %d: job %d\n", id, j)
		time.Sleep(50 * time.Millisecond) // simulate work
		results <- j * 2
	}
}

func main() {
	// 1) Pipeline: each stage is a goroutine connected by unbuffered channels.
	for s := range square(generator(2, 3, 4, 5)) {
		fmt.Println("square:", s)
	}

	// 2) Fan-out / fan-in with a WaitGroup so we never count receives blindly.
	jobs := make(chan int, 10)
	results := make(chan int, 10)

	var wg sync.WaitGroup
	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	for j := 1; j <= 9; j++ {
		jobs <- j
	}
	close(jobs) // no more work

	go func() {
		wg.Wait()      // all workers drained jobs
		close(results) // now it's safe to signal "no more results"
	}()

	for r := range results {
		fmt.Println("result:", r)
	}
}
