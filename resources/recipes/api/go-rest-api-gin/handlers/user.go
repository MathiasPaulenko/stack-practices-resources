package handlers

import (
	"net/http"

	"example.com/go-rest-api-gin/middleware"
	"github.com/gin-gonic/gin"
)

type CreateUserRequest struct {
	Name  string `json:"name" binding:"required,min=2,max=50"`
	Email string `json:"email" binding:"required,email"`
	Age   int    `json:"age" binding:"gte=0,lte=150"`
}

func ListUsers(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"users": []string{"alice", "bob"}})
}

func GetUser(c *gin.Context) {
	id := c.Param("id")
	c.JSON(http.StatusOK, gin.H{"id": id})
}

func CreateUser(c *gin.Context) {
	var req CreateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.Error(&middleware.APIError{Code: "validation_failed", Message: err.Error(), Status: http.StatusBadRequest})
		return
	}

	user := gin.H{"id": 1, "name": req.Name, "email": req.Email, "age": req.Age}
	c.JSON(http.StatusCreated, user)
}

func Health(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "healthy"})
}
