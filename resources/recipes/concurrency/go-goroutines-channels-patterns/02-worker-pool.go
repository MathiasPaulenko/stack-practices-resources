package main

import (
	"fmt"
	"sync"
)

type Job struct {
	ID    int
	Input string
}

type Result struct {
	JobID  int
	Output string
	Err    error
}

func worker(id int, jobs <-chan Job, results chan<- Result, wg *sync.WaitGroup) {
	defer wg.Done()
	for job := range jobs {
		// Process job
		output, err := process(job.Input)
		results <- Result{
			JobID:  job.ID,
			Output: output,
			Err:    err,
		}
	}
}

func process(input string) (string, error) {
	return "processed:" + input, nil
}

func runWorkerPool(numWorkers, numJobs int) []Result {
	jobs := make(chan Job, numJobs)
	results := make(chan Result, numJobs)
	var wg sync.WaitGroup

	// Launch workers
	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	// Send jobs
	for j := 0; j < numJobs; j++ {
		jobs <- Job{ID: j, Input: fmt.Sprintf("task-%d", j)}
	}
	close(jobs)

	// Wait and collect
	go func() {
		wg.Wait()
		close(results)
	}()

	var allResults []Result
	for r := range results {
		allResults = append(allResults, r)
	}
	return allResults
}

func main() {
	results := runWorkerPool(5, 20)
	fmt.Printf("Processed %d jobs\n", len(results))
}
