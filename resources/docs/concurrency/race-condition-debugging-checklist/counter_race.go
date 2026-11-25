// Go -race demo: unsynchronized increment from many goroutines (section 3.2).
//
// Run with the race detector:
//
//	go run -race counter_race.go
//
// The detector reports two conflicting accesses to the same address with
// the stacks that produced them — fix that pair, not the crash site.
package main

import (
	"fmt"
	"sync"
)

var count int

func increment() {
	count++ // DATA RACE: read-modify-write, not atomic
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
	fmt.Println("final count:", count) // usually < 100000
}
