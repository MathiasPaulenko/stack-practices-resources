# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /build

COPY go.mod ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o server .

# Stage 2: Runtime (scratch = empty image)
FROM scratch AS runtime

COPY --from=builder /build/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080

ENTRYPOINT ["/server"]
