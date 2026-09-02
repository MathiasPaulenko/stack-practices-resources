package com.example.grpc;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;
import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class Client {
    public static void main(String[] args) throws Exception {
        ManagedChannel channel = ManagedChannelBuilder
            .forAddress("localhost", 50051)
            .usePlaintext()
            .build();

        GreeterGrpc.GreeterBlockingStub blockingStub = GreeterGrpc.newBlockingStub(channel);

        // Unary call
        HelloResponse response = blockingStub.sayHello(
            HelloRequest.newBuilder().setName("World").build());
        System.out.println("Unary: " + response.getMessage());

        // Streaming call
        GreeterGrpc.GreeterStub asyncStub = GreeterGrpc.newStub(channel);
        CountDownLatch latch = new CountDownLatch(1);

        StreamObserver<HelloRequest> requestObserver = asyncStub.streamGreetings(
            new StreamObserver<HelloResponse>() {
                @Override
                public void onNext(HelloResponse response) {
                    System.out.println("Streaming: " + response.getMessage());
                }

                @Override
                public void onError(Throwable t) {
                    System.err.println("Stream error: " + t.getMessage());
                    latch.countDown();
                }

                @Override
                public void onCompleted() {
                    System.out.println("Stream complete");
                    latch.countDown();
                }
            });

        for (String name : Arrays.asList("Alice", "Bob", "Charlie")) {
            requestObserver.onNext(HelloRequest.newBuilder().setName(name).build());
        }
        requestObserver.onCompleted();

        latch.await(5, TimeUnit.SECONDS);
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }
}
