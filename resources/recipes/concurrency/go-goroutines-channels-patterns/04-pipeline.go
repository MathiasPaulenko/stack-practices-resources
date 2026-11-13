package main

import "fmt"

// Multi-stage pipeline: generate → filter → transform → collect

func generate(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for _, n := range nums {
			out <- n
		}
	}()
	return out
}

func filter(in <-chan int, predicate func(int) bool) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			if predicate(n) {
				out <- n
			}
		}
	}()
	return out
}

func transform(in <-chan int, fn func(int) int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			out <- fn(n)
		}
	}()
	return out
}

func main() {
	// Pipeline: generate → filter even → square → print
	nums := generate(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
	evens := filter(nums, func(n int) bool { return n%2 == 0 })
	squared := transform(evens, func(n int) int { return n * n })

	for result := range squared {
		fmt.Printf("Even squared: %d\n", result)
	}
}
