// HMAC-SHA256 request signing — sign and verify with replay window.
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"net/http"
	"time"
)

func SignRequest(secret, method, path, body string) http.Header {
	timestamp := time.Now().UTC().Format(time.RFC3339)
	message := fmt.Sprintf("%s\n%s\n%s\n%s", method, path, timestamp, body)

	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(message))
	signature := hex.EncodeToString(mac.Sum(nil))

	header := http.Header{}
	header.Set("X-Request-Timestamp", timestamp)
	header.Set("X-Request-Signature", signature)
	return header
}

func VerifyRequest(secret string, r *http.Request, body []byte) bool {
	timestamp := r.Header.Get("X-Request-Timestamp")
	signature := r.Header.Get("X-Request-Signature")

	ts, err := time.Parse(time.RFC3339, timestamp)
	if err != nil {
		return false
	}
	if time.Since(ts) > 5*time.Minute {
		return false
	}

	message := fmt.Sprintf("%s\n%s\n%s\n%s",
		r.Method, r.URL.Path, timestamp, string(body))

	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(message))
	expected := hex.EncodeToString(mac.Sum(nil))

	return hmac.Equal([]byte(signature), []byte(expected))
}
