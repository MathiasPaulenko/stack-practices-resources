package main

import (
	"fmt"
	"sync"
)

// Fan-out: distribute work to multiple goroutines
// Fan-in: merge results from multiple goroutines into one channel

func producer(start, end int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := start; i <= end; i++ {
			out <- i
		}
	}()
	return out
}

func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			out <- n * n
		}
	}()
	return out
}

// Fan-in: merge multiple channels into one
func merge(channels ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)

	output := func(c <-chan int) {
		defer wg.Done()
		for n := range c {
			out <- n
		}
	}

	wg.Add(len(channels))
	for _, c := range channels {
		go output(c)
	}

	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func main() {
	// Fan-out: 4 workers processing the same input
	input := producer(1, 100)

	squared1 := square(input)
	squared2 := square(input)
	squared3 := square(input)
	squared4 := square(input)

	// Fan-in: merge all squared outputs
	for result := range merge(squared1, squared2, squared3, squared4) {
		fmt.Printf("Result: %d\n", result)
	}
}
