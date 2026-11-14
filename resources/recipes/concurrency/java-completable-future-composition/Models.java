import java.util.List;

// Domain records shared by all examples (package-private, Java 17+).
record User(String id, String name) {}

record Order(String id, String userId, double total) {}

record UserProfile(User user, List<Order> orders) {}

record Notification(String id, String text) {}

record PartialDashboard(User user, List<Order> orders) {}

record Dashboard(User user, List<Order> orders, List<Notification> notifications) {}

record SalesData(String userId, String range, double total) {
    static final SalesData EMPTY = new SalesData("", "", 0);
}

record TrafficData(String userId, String range, long visits) {}

record RevenueData(String userId, String range, double revenue) {}

record AggregatedReport(SalesData sales, TrafficData traffic, RevenueData revenue) {}
