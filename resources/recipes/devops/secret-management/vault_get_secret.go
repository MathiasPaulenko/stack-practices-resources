package main

import (
	"context"
	"fmt"
	"os"

	"github.com/hashicorp/vault/api"
)

func main() {
	client, err := api.NewClient(api.DefaultConfig())
	if err != nil {
		panic(err)
	}
	// Token comes from the environment (Vault Agent, workload identity) — never hardcoded
	client.SetToken(os.Getenv("VAULT_TOKEN"))

	secret, err := client.KVv2("secret").Get(context.Background(), "database/creds")
	if err != nil {
		panic(err)
	}
	fmt.Println("username:", secret.Data["username"])
}
