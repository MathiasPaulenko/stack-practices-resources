// Leader election against the Kubernetes Lease API with client-go.
//
// Companion code for https://stackpractices.com/patterns/leader-election-pattern/
//
// In production prefer k8s.io/client-go/tools/leaderelection.RunOrDie;
// this file shows the update loop that package runs internally.
package main

import (
	"context"
	"fmt"
	"time"

	coordinationv1 "k8s.io/api/coordination/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

type LeaseLeaderElection struct {
	clientset      *kubernetes.Clientset
	leaseName      string
	leaseNamespace string
	holderIdentity string
	leaseDuration  time.Duration
}

func NewLeaseLeaderElection(leaseName, namespace, holderIdentity string, duration time.Duration) (*LeaseLeaderElection, error) {
	config, err := rest.InClusterConfig()
	if err != nil {
		return nil, err
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, err
	}

	return &LeaseLeaderElection{
		clientset:      clientset,
		leaseName:      leaseName,
		leaseNamespace: namespace,
		holderIdentity: holderIdentity,
		leaseDuration:  duration,
	}, nil
}

func (l *LeaseLeaderElection) Acquire(ctx context.Context) error {
	lease := &coordinationv1.Lease{
		ObjectMeta: metav1.ObjectMeta{
			Name:      l.leaseName,
			Namespace: l.leaseNamespace,
		},
		Spec: coordinationv1.LeaseSpec{
			HolderIdentity:       &l.holderIdentity,
			LeaseDurationSeconds: pointerToInt32(int32(l.leaseDuration.Seconds())),
			AcquireTime:          &metav1.Time{Time: time.Now()},
			RenewTime:            &metav1.Time{Time: time.Now()},
		},
	}

	for {
		current, err := l.clientset.CoordinationV1().Leases(l.leaseNamespace).Get(ctx, l.leaseName, metav1.GetOptions{})
		if err != nil {
			// Lease doesn't exist, try to create
			_, err = l.clientset.CoordinationV1().Leases(l.leaseNamespace).Create(ctx, lease, metav1.CreateOptions{})
			if err == nil {
				return nil // Acquired leadership
			}
			time.Sleep(time.Second)
			continue
		}

		// Check if lease is expired or we are the holder
		if current.Spec.HolderIdentity == nil || *current.Spec.HolderIdentity == l.holderIdentity {
			// Renew lease
			current.Spec.HolderIdentity = &l.holderIdentity
			current.Spec.RenewTime = &metav1.Time{Time: time.Now()}
			_, err = l.clientset.CoordinationV1().Leases(l.leaseNamespace).Update(ctx, current, metav1.UpdateOptions{})
			if err == nil {
				return nil // Leadership maintained
			}
		}

		time.Sleep(time.Second)
	}
}

func (l *LeaseLeaderElection) Renew(ctx context.Context) error {
	ticker := time.NewTicker(l.leaseDuration / 2)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			lease, err := l.clientset.CoordinationV1().Leases(l.leaseNamespace).Get(ctx, l.leaseName, metav1.GetOptions{})
			if err != nil {
				return fmt.Errorf("failed to get lease: %w", err)
			}

			if lease.Spec.HolderIdentity == nil || *lease.Spec.HolderIdentity != l.holderIdentity {
				return fmt.Errorf("lost leadership")
			}

			lease.Spec.RenewTime = &metav1.Time{Time: time.Now()}
			_, err = l.clientset.CoordinationV1().Leases(l.leaseNamespace).Update(ctx, lease, metav1.UpdateOptions{})
			if err != nil {
				return fmt.Errorf("failed to renew lease: %w", err)
			}

		case <-ctx.Done():
			return nil
		}
	}
}

func pointerToInt32(i int32) *int32 {
	return &i
}
