// The mutex fix for counter_race.go (sections 4.2 and 5.1).
//
//	go run -race counter_fix.go
//
// The lock wraps the whole read-modify-write; `go run -race` stays silent.
package main

import (
	"fmt"
	"sync"
)

var (
	mu    sync.Mutex
	count int
)

func increment() {
	mu.Lock()
	count++
	mu.Unlock()
}

func main() {
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 1000; j++ {
				increment()
			}
		}()
	}
	wg.Wait()
	fmt.Println("final count:", count) // always 100000
}
