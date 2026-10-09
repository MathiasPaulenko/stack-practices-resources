package main

// Generate URL-friendly slugs using golang.org/x/text normalization.
// Requires: go get golang.org/x/text

import (
	"fmt"
	"regexp"
	"strings"
	"unicode"

	"golang.org/x/text/unicode/norm"
)

func generateSlug(text string) string {
	t := norm.NFKD.String(text)

	var b strings.Builder
	for _, r := range t {
		if unicode.Is(unicode.Mn, r) {
			continue
		}
		b.WriteRune(r)
	}
	text = strings.ToLower(b.String())

	reg := regexp.MustCompile(`[^a-z0-9]+`)
	text = reg.ReplaceAllString(text, "-")

	return strings.Trim(text, "-")
}

func main() {
	fmt.Println(generateSlug("Hello, World! 2024"))   // hello-world-2024
	fmt.Println(generateSlug("Café & Crème Brûlée"))  // cafe-creme-brulee
}
