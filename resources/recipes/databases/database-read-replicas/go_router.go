// Package db provides a read/write splitting router for PostgreSQL.
//
// Usage:
//   router, err := NewDBRouter("postgres://user:pass@primary:5432/app", []string{
//       "postgres://user:pass@replica1:5432/app",
//       "postgres://user:pass@replica2:5432/app",
//   })
//   ...
//   rows, err := router.Read().Query("SELECT id, email FROM users WHERE id = $1", 1)
//   _, err = router.Write().Exec("INSERT INTO users (email) VALUES ($1)", "alice@example.com")

package db

import (
	"database/sql"
	"math/rand"
	"time"

	_ "github.com/lib/pq"
)

type DBRouter struct {
	primary  *sql.DB
	replicas []*sql.DB
	rng      *rand.Rand
}

func NewDBRouter(primaryURL string, replicaURLs []string) (*DBRouter, error) {
	primary, err := sql.Open("postgres", primaryURL)
	if err != nil {
		return nil, err
	}
	primary.SetMaxOpenConns(20)

	replicas := make([]*sql.DB, len(replicaURLs))
	for i, url := range replicaURLs {
		replica, err := sql.Open("postgres", url)
		if err != nil {
			return nil, err
		}
		replica.SetMaxOpenConns(10)
		replicas[i] = replica
	}

	return &DBRouter{
		primary:  primary,
		replicas: replicas,
		rng:      rand.New(rand.NewSource(time.Now().UnixNano())),
	}, nil
}

func (r *DBRouter) Read() *sql.DB {
	if len(r.replicas) == 0 {
		return r.primary
	}
	return r.replicas[r.rng.Intn(len(r.replicas))]
}

func (r *DBRouter) Write() *sql.DB {
	return r.primary
}

func (r *DBRouter) Close() {
	r.primary.Close()
	for _, rep := range r.replicas {
		rep.Close()
	}
}
