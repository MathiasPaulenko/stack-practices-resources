package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"example.com/go-rest-api-gin/middleware"
	"github.com/gin-gonic/gin"
)

func setupRouter() *gin.Engine {
	gin.SetMode(gin.TestMode)

	r := gin.New()
	r.Use(middleware.ErrorHandler())

	api := r.Group("/api/v1")
	{
		api.GET("/users", ListUsers)
		api.GET("/users/:id", GetUser)
		api.POST("/users", CreateUser)
		api.GET("/health", Health)
	}

	return r
}

func TestListUsers(t *testing.T) {
	router := setupRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/v1/users", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	if !strings.Contains(w.Body.String(), "alice") || !strings.Contains(w.Body.String(), "bob") {
		t.Fatalf("expected users in response, got %s", w.Body.String())
	}
}

func TestGetUser(t *testing.T) {
	router := setupRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/v1/users/42", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	if !strings.Contains(w.Body.String(), "42") {
		t.Fatalf("expected user id in response, got %s", w.Body.String())
	}
}

func TestCreateUser(t *testing.T) {
	router := setupRouter()

	body := `{"name":"alice","email":"alice@example.com","age":30}`
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/users", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	if w.Code != http.StatusCreated {
		t.Fatalf("expected 201, got %d: %s", w.Code, w.Body.String())
	}

	var resp map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
		t.Fatalf("invalid JSON response: %v", err)
	}
	if resp["name"] != "alice" || resp["email"] != "alice@example.com" || resp["age"] != float64(30) {
		t.Fatalf("unexpected response: %v", resp)
	}
}

func TestCreateUserValidation(t *testing.T) {
	router := setupRouter()

	body := `{"name":"a","email":"not-an-email","age":200}`
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/users", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	router.ServeHTTP(w, req)

	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d: %s", w.Code, w.Body.String())
	}
	if !strings.Contains(w.Body.String(), "validation_failed") {
		t.Fatalf("expected validation_failed in response, got %s", w.Body.String())
	}
}

func TestHealth(t *testing.T) {
	router := setupRouter()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/health", nil)
	router.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	if !strings.Contains(w.Body.String(), "healthy") {
		t.Fatalf("expected healthy status, got %s", w.Body.String())
	}
}
