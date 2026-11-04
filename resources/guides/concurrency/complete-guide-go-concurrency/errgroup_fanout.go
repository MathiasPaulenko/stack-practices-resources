// errgroup_fanout.go — fan-out with first-error cancellation
package main

import ("context"; "golang.org/x/sync/errgroup")

func fanout(ctx context.Context, urls []string) error {
	g, ctx := errgroup.WithContext(ctx)
	for _, u := range urls {
		u := u
		g.Go(func() error { return fetch(ctx, u) })
	}
	return g.Wait()
}
