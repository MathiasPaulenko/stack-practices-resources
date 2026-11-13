package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"net/http"
	"sync/atomic"
	"time"

	_ "github.com/lib/pq"
	"github.com/redis/go-redis/v9"
)

type HealthStatus struct {
	Status string          `json:"status"`
	Checks map[string]bool `json:"checks"`
}

var db *sql.DB
var rdb *redis.Client
var appReady atomic.Bool

func checkDB() bool {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	return db.PingContext(ctx) == nil
}

func checkRedis() bool {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	return rdb.Ping(ctx).Err() == nil
}

func livenessHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(HealthStatus{Status: "alive"})
}

func startupHandler(w http.ResponseWriter, r *http.Request) {
	if !appReady.Load() {
		w.WriteHeader(http.StatusServiceUnavailable)
		return
	}
	w.WriteHeader(http.StatusOK)
}

func readinessHandler(w http.ResponseWriter, r *http.Request) {
	checks := map[string]bool{
		"db":    checkDB(),
		"redis": checkRedis(),
	}
	allOK := true
	for _, ok := range checks {
		if !ok {
			allOK = false
		}
	}
	w.Header().Set("Content-Type", "application/json")
	if allOK {
		w.WriteHeader(http.StatusOK)
	} else {
		w.WriteHeader(http.StatusServiceUnavailable)
	}
	status := "not ready"
	if allOK {
		status = "ready"
	}
	json.NewEncoder(w).Encode(HealthStatus{Status: status, Checks: checks})
}

func main() {
	// ... open db and rdb, run migrations, warm caches ...
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if db.PingContext(ctx) == nil {
		appReady.Store(true)
	}

	http.HandleFunc("/health/live", livenessHandler)
	http.HandleFunc("/health/startup", startupHandler)
	http.HandleFunc("/health/ready", readinessHandler)
	http.ListenAndServe(":8080", nil)
}
