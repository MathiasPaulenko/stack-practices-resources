public class OrderHandler implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
    // Runs during snapshot creation, not on every cold start
    private static final OrderService orderService = initOrderService();

    private static OrderService initOrderService() {
        return new OrderService(DynamoDbClient.builder().build(), new ObjectMapper(), loadConfiguration());
    }

    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent event, Context context) {
        // Handler path stays fast because init was snapshotted
        return orderService.process(event);
    }
}
