package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// GET request with Go net/http — context timeout, status check, body close.
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, "GET", "https://api.example.com/users/1", nil)
	if err != nil {
		fmt.Printf("Failed to build request: %v\n", err)
		return
	}
	req.Header.Set("Accept", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf("Request failed: %v\n", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		fmt.Printf("HTTP %d\n", resp.StatusCode)
		return
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read body: %v\n", err)
		return
	}

	var data map[string]interface{}
	if err := json.Unmarshal(body, &data); err != nil {
		fmt.Printf("Failed to parse JSON: %v\n", err)
		return
	}

	fmt.Println(data["name"])
}
