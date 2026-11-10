# Multi-stage Go build ending on distroless static.
# Build: docker build -f Dockerfile.go -t app:distroless .
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod ./
RUN go mod download

COPY . .
# CGO must be off: distroless/static ships no libc at all.
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server .

FROM gcr.io/distroless/static-debian12:nonroot

COPY --from=builder /app/server /server

EXPOSE 8080

# The image already runs as nonroot (uid 65532) via the :nonroot tag.
ENTRYPOINT ["/server"]
