// Health endpoint with split liveness and readiness probes.
//
// A service that fails liveness gets restarted; one that fails readiness
// stays alive but drops out of the discovery pool — which is what you
// want during warm-up or while a downstream dependency is down.
package main

import (
	"net/http"
	"sync/atomic"
	"time"
)

type HealthChecker struct {
	ready     atomic.Bool
	lastCheck atomic.Int64
}

func (h *HealthChecker) LivenessHandler(w http.ResponseWriter, r *http.Request) {
	// Liveness: is the process alive?
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"alive"}`))
}

func (h *HealthChecker) ReadinessHandler(w http.ResponseWriter, r *http.Request) {
	// Readiness: can we handle requests?
	last := h.lastCheck.Load()
	if time.Now().UnixMilli()-last > 10000 {
		w.WriteHeader(http.StatusServiceUnavailable)
		w.Write([]byte(`{"status":"not ready"}`))
		return
	}
	if !h.ready.Load() {
		w.WriteHeader(http.StatusServiceUnavailable)
		w.Write([]byte(`{"status":"starting"}`))
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"ready"}`))
}

func (h *HealthChecker) StartHealthCheckLoop() {
	ticker := time.NewTicker(5 * time.Second)
	go func() {
		for range ticker.C {
			ok := checkDatabaseConnection()
			h.ready.Store(ok)
			h.lastCheck.Store(time.Now().UnixMilli())
		}
	}()
}

func checkDatabaseConnection() bool {
	// Placeholder: ping your dependency with a short timeout.
	return true
}

func main() {
	hc := &HealthChecker{}
	hc.StartHealthCheckLoop()
	http.HandleFunc("/health", hc.LivenessHandler)
	http.HandleFunc("/ready", hc.ReadinessHandler)
	http.ListenAndServe(":8080", nil)
}
