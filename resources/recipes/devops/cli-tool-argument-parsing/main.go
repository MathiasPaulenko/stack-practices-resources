package main

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var (
    version string
    dryRun  bool
    verbose bool
)

func main() {
    rootCmd := &cobra.Command{
        Use:     "deploy-cli",
        Short:   "CLI for app deployments",
        Version: "1.0.0",
    }

    deployCmd := &cobra.Command{
        Use:   "deploy [environment]",
        Short: "Deploy to an environment",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            env := args[0]
            fmt.Printf("Deploying %s to %s\n", version, env)
            if dryRun {
                fmt.Println("(dry run mode)")
            }
        },
    }

    deployCmd.Flags().StringVarP(&version, "version", "v", "latest", "App version")
    deployCmd.Flags().BoolVar(&dryRun, "dry-run", false, "Simulate without changes")
    deployCmd.Flags().BoolVarP(&verbose, "verbose", "V", false, "Verbose output")

    rootCmd.AddCommand(deployCmd)
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}
