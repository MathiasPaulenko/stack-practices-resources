package main

import (
	"fmt"
	"net/http"
	"golang.org/x/sync/errgroup"
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

func main() {
	urls := []string{
		"https://api.example.com/users",
		"https://api.example.com/orders",
		"https://api.example.com/products",
	}

	var g errgroup.Group

	for _, url := range urls {
		url := url // Capture loop variable
		g.Go(func() error {
			return fetchURL(url)
		})
	}

	// Wait for all goroutines: returns first error
	if err := g.Wait(); err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Println("All fetches succeeded")
	}
}
