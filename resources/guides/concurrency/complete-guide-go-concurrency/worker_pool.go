// worker_pool.go — fixed pool draining a jobs channel with graceful shutdown
package main

import ("context"; "sync")

func worker(ctx context.Context, id int, jobs <-chan Job, results chan<- Result, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-ctx.Done():
			return
		case job, ok := <-jobs:
			if !ok { return }
			results <- job.Process(ctx)
		}
	}
}
