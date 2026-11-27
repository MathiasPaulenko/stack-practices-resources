// Consul service registration with graceful deregistration on SIGTERM.
//
// Registers the service with an HTTP health check and
// DeregisterCriticalServiceAfter, so a crashed process that never
// deregisters is removed from the catalog automatically.
package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/hashicorp/consul/api"
)

func registerService(consulAddr, serviceID, name, host string, port int) (*api.Client, error) {
	config := api.DefaultConfig()
	config.Address = consulAddr
	client, err := api.NewClient(config)
	if err != nil {
		return nil, err
	}

	registration := &api.AgentServiceRegistration{
		ID:      serviceID,
		Name:    name,
		Address: host,
		Port:    port,
		Check: &api.AgentServiceCheck{
			HTTP:     fmt.Sprintf("http://%s:%d/health", host, port),
			Interval: "10s",
			Timeout:  "5s",
			// Remove the entry if the service dies without deregistering.
			DeregisterCriticalServiceAfter: "90s",
		},
	}

	if err := client.Agent().ServiceRegister(registration); err != nil {
		return nil, err
	}
	return client, nil
}

func main() {
	client, err := registerService("localhost:8500", "payment-01", "payment-service", "10.0.3.7", 8080)
	if err != nil {
		panic(err)
	}

	// Graceful shutdown: deregister first, drain, then exit.
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGTERM, syscall.SIGINT)
	<-sig

	if err := client.Agent().ServiceDeregister("payment-01"); err != nil {
		fmt.Fprintln(os.Stderr, "deregistration failed:", err)
	}
}
