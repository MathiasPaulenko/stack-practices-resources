// semaphore.go — buffered channel semaphore: max N concurrent tasks
package main

import "sync"

var sem = make(chan struct{}, 10) // capacity = max concurrency

func processAll(tasks []Task) {
	var wg sync.WaitGroup
	for _, t := range tasks {
		wg.Add(1)
		go func(task Task) {
			defer wg.Done()
			sem <- struct{}{}        // acquire
			defer func() { <-sem }() // release
			task.Run()
		}(t)
	}
	wg.Wait()
}
