package main

import (
	"log"
	"net/http"

	"example.com/go-rest-api-gin/handlers"
	"example.com/go-rest-api-gin/middleware"
	"example.com/go-rest-api-gin/server"
	"github.com/gin-gonic/gin"
)

func main() {
	gin.SetMode(gin.ReleaseMode)

	r := gin.New()
	r.Use(middleware.Logger(), gin.Recovery(), middleware.ErrorHandler())

	api := r.Group("/api/v1")
	api.Use(middleware.AuthRequired())
	{
		api.GET("/users", handlers.ListUsers)
		api.GET("/users/:id", handlers.GetUser)
		api.POST("/users", handlers.CreateUser)
		api.GET("/health", handlers.Health)
	}

	if err := server.RunWithGracefulShutdown(r, ":8080"); err != nil {
		log.Fatalf("server shutdown: %s", err)
	}
}
