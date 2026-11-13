package main

import (
	"fmt"
	"time"
)

func tee[T any](in <-chan T) (<-chan T, <-chan T) {
	out1 := make(chan T)
	out2 := make(chan T)
	go func() {
		defer close(out1)
		defer close(out2)
		for val := range in {
			out1 <- val
			out2 <- val
		}
	}()
	return out1, out2
}

func main() {
	in := make(chan int, 3)
	a, b := tee(in)
	in <- 1
	in <- 2
	close(in)
	fmt.Println(<-a, <-b)
	time.Sleep(10 * time.Millisecond)
	fmt.Println(<-a, <-b)
}
