// Parse and validate YAML/JSON config in Go

package main

import (
	"encoding/json"
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

type DatabaseConfig struct {
	Host     string `json:"host" yaml:"host"`
	Port     int    `json:"port" yaml:"port"`
	Username string `json:"username" yaml:"username"`
	Password string `json:"password" yaml:"password"`
}

type AppConfig struct {
	AppName  string         `json:"appName" yaml:"appName"`
	Debug    bool           `json:"debug" yaml:"debug"`
	Database DatabaseConfig `json:"database" yaml:"database"`
}

func loadConfig(path string) (*AppConfig, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read file: %w", err)
	}

	var config AppConfig
	if len(path) > 5 && path[len(path)-5:] == ".json" {
		err = json.Unmarshal(data, &config)
	} else {
		err = yaml.Unmarshal(data, &config)
	}
	if err != nil {
		return nil, fmt.Errorf("parse: %w", err)
	}

	if config.Database.Host == "" || config.Database.Port == 0 {
		return nil, fmt.Errorf("database.host and database.port are required")
	}
	return &config, nil
}

func main() {
	config, err := loadConfig("config.yaml")
	if err != nil {
		fmt.Printf("Config validation failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("App: %s\n", config.AppName)
	fmt.Printf("DB host: %s\n", config.Database.Host)
}
