// gRPC UserService client in Go — companion to
// https://stackpractices.com/guides/grpc-microservices-guide/
// Generate stubs with: protoc -I. --go_out=. --go-grpc_out=. user_service.proto
package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "user-service/proto"
)

func main() {
	// insecure.NewCredentials() is the post-1.40 API (grpc.WithInsecure is
	// deprecated). Production: credentials.NewTLS(&tls.Config{...})
	conn, err := grpc.Dial("localhost:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	client := pb.NewUserServiceClient(conn)

	// Deadline on every call — the default is infinite
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	resp, err := client.GetUser(ctx, &pb.GetUserRequest{UserId: "1"})
	if err != nil {
		log.Fatalf("could not get user: %v", err)
	}
	log.Printf("User: %s <%s>", resp.Name, resp.Email)
}
