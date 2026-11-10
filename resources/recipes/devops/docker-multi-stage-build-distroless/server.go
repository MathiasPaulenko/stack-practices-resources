package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
)

// Minimal static Go server. The --healthcheck flag doubles as the
// container HEALTHCHECK command, since distroless has no curl/wget.
func main() {
	healthcheck := flag.Bool("healthcheck", false, "exit 0 if the server is healthy")
	flag.Parse()

	if *healthcheck {
		resp, err := http.Get("http://localhost:8080/health")
		if err != nil || resp.StatusCode != http.StatusOK {
			os.Exit(1)
		}
		os.Exit(0)
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "ok")
	})
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "hello from distroless")
	})

	fmt.Println("listening on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
