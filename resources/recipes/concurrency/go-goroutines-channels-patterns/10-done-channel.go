package main

import (
	"fmt"
	"time"
)

type Job struct {
	ID    int
	Input string
}

func process(j Job) {
	fmt.Printf("processing job %d (%s)
", j.ID, j.Input)
}

func worker(done <-chan struct{}, jobs <-chan Job) {
	for {
		select {
		case <-done:
			return
		case job := <-jobs:
			process(job)
		}
	}
}

func main() {
	jobs := make(chan Job, 5)
	for i := 0; i < 5; i++ {
		jobs <- Job{ID: i, Input: fmt.Sprintf("task-%d", i)}
	}

	// Cancel by closing the done channel
	done := make(chan struct{})
	go worker(done, jobs)
	time.Sleep(500 * time.Millisecond)
	close(done) // Signals all workers to stop
}
