// Bulkhead pattern with semaphores and errgroup (Go).
// Companion to https://stackpractices.com/recipes/microservices-patterns/
// Each downstream dependency gets a bounded concurrency lane so a slow
// service degrades only its own lane.
package main

import (
	"context"
	"fmt"
	"time"

	"golang.org/x/sync/errgroup"
)

type Bulkhead struct {
	sem chan struct{}
}

func NewBulkhead(maxConcurrent int) *Bulkhead {
	return &Bulkhead{sem: make(chan struct{}, maxConcurrent)}
}

func (b *Bulkhead) Execute(ctx context.Context, fn func() error) error {
	select {
	case b.sem <- struct{}{}:
		defer func() { <-b.sem }()
		return fn()
	case <-ctx.Done():
		return ctx.Err()
	}
}

type Order struct {
	ID    string
	Items []string
	Total float64
}

type ResilientClient struct {
	paymentBulkhead   *Bulkhead
	inventoryBulkhead *Bulkhead
	shippingBulkhead  *Bulkhead
}

func NewResilientClient() *ResilientClient {
	return &ResilientClient{
		paymentBulkhead:   NewBulkhead(10),
		inventoryBulkhead: NewBulkhead(20),
		shippingBulkhead:  NewBulkhead(5),
	}
}

func (c *ResilientClient) ProcessOrder(ctx context.Context, order Order) error {
	g, ctx := errgroup.WithContext(ctx)

	g.Go(func() error {
		return c.paymentBulkhead.Execute(ctx, func() error {
			return c.callPaymentService(ctx, order)
		})
	})

	g.Go(func() error {
		return c.inventoryBulkhead.Execute(ctx, func() error {
			return c.callInventoryService(ctx, order)
		})
	})

	if err := g.Wait(); err != nil {
		return fmt.Errorf("order processing failed: %w", err)
	}

	return c.shippingBulkhead.Execute(ctx, func() error {
		return c.callShippingService(ctx, order)
	})
}

func (c *ResilientClient) callPaymentService(ctx context.Context, order Order) error {
	ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()
	// HTTP call to payment service
	return nil
}

func (c *ResilientClient) callInventoryService(ctx context.Context, order Order) error {
	ctx, cancel := context.WithTimeout(ctx, 1*time.Second)
	defer cancel()
	// HTTP call to inventory service
	return nil
}

func (c *ResilientClient) callShippingService(ctx context.Context, order Order) error {
	ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
	defer cancel()
	// HTTP call to shipping service
	return nil
}

func main() {
	client := NewResilientClient()
	ctx := context.Background()
	if err := client.ProcessOrder(ctx, Order{ID: "ord_123"}); err != nil {
		fmt.Println(err)
	}
}
