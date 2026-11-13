package main

import (
	"fmt"
	"net/http"
	"sync"
)

func fetchURL(url string) error {
	resp, err := http.Get(url)
	if err != nil {
		return fmt.Errorf("fetch %s: %w", url, err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return fmt.Errorf("fetch %s: status %d", url, resp.StatusCode)
	}
	return nil
}

func boundedParallel(urls []string, maxConcurrent int) []error {
	sem := make(chan struct{}, maxConcurrent)
	errs := make([]error, len(urls))
	var wg sync.WaitGroup

	for i, url := range urls {
		wg.Add(1)
		go func(idx int, u string) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire
			defer func() { <-sem }() // Release
			errs[idx] = fetchURL(u)
		}(i, url)
	}

	wg.Wait()
	return errs
}

func main() {
	urls := []string{
		"https://api.example.com/users",
		"https://api.example.com/orders",
		"https://api.example.com/products",
		"https://api.example.com/inventory",
		"https://api.example.com/stats",
	}
	for i, err := range boundedParallel(urls, 2) {
		fmt.Printf("url %d: %v
", i, err)
	}
}
