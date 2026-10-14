// In-app scheduling with robfig/cron v3.
// Run: go mod init example && go get github.com/robfig/cron/v3 && go run main.go
package main

import (
	"fmt"
	"time"

	"github.com/robfig/cron/v3"
)

func main() {
	c := cron.New()

	// Every 15 minutes
	c.AddFunc("*/15 * * * *", func() {
		fmt.Println("Health check running...")
	})

	// Every day at 3:00 AM
	c.AddFunc("0 3 * * *", func() {
		fmt.Println("Daily backup running...")
	})

	// With seconds field (requires cron.New(cron.WithSeconds()))
	// s := cron.New(cron.WithSeconds())
	// s.AddFunc("*/10 * * * * *", func() { ... }) // Every 10 seconds

	c.Start()
	fmt.Println("Scheduler started at", time.Now().Format(time.RFC3339))
	select {} // Block forever
}
