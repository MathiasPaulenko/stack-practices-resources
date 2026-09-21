import java.sql.*;
import java.util.*;

// Composite Entity Pattern — Order + LineItem + ShippingAddress persisted
// as one unit across three tables. Compile with the SQLite JDBC driver on
// the classpath (or adapt the URL/queries to your database).

class LineItem {
    private final String productId;
    private final int quantity;
    private final double unitPrice;

    public LineItem(String productId, int quantity, double unitPrice) {
        this.productId = productId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    public double getTotal() { return quantity * unitPrice; }
    public String getProductId() { return productId; }
    public int getQuantity() { return quantity; }
    public double getUnitPrice() { return unitPrice; }
}

class ShippingAddress {
    private final String street, city, country, postalCode;

    public ShippingAddress(String street, String city, String country, String postalCode) {
        this.street = street;
        this.city = city;
        this.country = country;
        this.postalCode = postalCode;
    }

    public String getStreet() { return street; }
    public String getCity() { return city; }
    public String getCountry() { return country; }
    public String getPostalCode() { return postalCode; }
}

class Order {
    private final String orderId;
    private final String customerId;
    private final List<LineItem> lineItems = new ArrayList<>();
    private ShippingAddress shippingAddress;

    public Order(String orderId, String customerId) {
        this.orderId = orderId;
        this.customerId = customerId;
    }

    public String getOrderId() { return orderId; }
    public String getCustomerId() { return customerId; }
    public List<LineItem> getLineItems() { return lineItems; }
    public ShippingAddress getShippingAddress() { return shippingAddress; }
    public void setShippingAddress(ShippingAddress addr) { this.shippingAddress = addr; }
    public double getTotal() {
        return lineItems.stream().mapToDouble(LineItem::getTotal).sum();
    }
}

public class OrderMapper {
    private final Connection conn;

    public OrderMapper(Connection conn) { this.conn = conn; }

    public Order findById(String orderId) throws SQLException {
        try (PreparedStatement stmt = conn.prepareStatement(
                "SELECT customer_id FROM orders WHERE order_id = ?")) {
            stmt.setString(1, orderId);
            try (ResultSet rs = stmt.executeQuery()) {
                if (!rs.next()) return null;
                Order order = new Order(orderId, rs.getString("customer_id"));

                try (PreparedStatement itemStmt = conn.prepareStatement(
                        "SELECT product_id, quantity, unit_price FROM line_items WHERE order_id = ?")) {
                    itemStmt.setString(1, orderId);
                    try (ResultSet items = itemStmt.executeQuery()) {
                        while (items.next()) {
                            order.getLineItems().add(new LineItem(
                                items.getString("product_id"),
                                items.getInt("quantity"),
                                items.getDouble("unit_price")));
                        }
                    }
                }

                try (PreparedStatement addrStmt = conn.prepareStatement(
                        "SELECT street, city, country, postal_code FROM shipping_addresses WHERE order_id = ?")) {
                    addrStmt.setString(1, orderId);
                    try (ResultSet addr = addrStmt.executeQuery()) {
                        if (addr.next()) {
                            order.setShippingAddress(new ShippingAddress(
                                addr.getString("street"), addr.getString("city"),
                                addr.getString("country"), addr.getString("postal_code")));
                        }
                    }
                }
                return order;
            }
        }
    }

    public void save(Order order) throws SQLException {
        boolean auto = conn.getAutoCommit();
        conn.setAutoCommit(false);  // one transaction across all three tables
        try {
            try (PreparedStatement stmt = conn.prepareStatement(
                    "INSERT OR REPLACE INTO orders (order_id, customer_id) VALUES (?, ?)")) {
                stmt.setString(1, order.getOrderId());
                stmt.setString(2, order.getCustomerId());
                stmt.executeUpdate();
            }

            try (PreparedStatement del = conn.prepareStatement(
                    "DELETE FROM line_items WHERE order_id = ?")) {
                del.setString(1, order.getOrderId());
                del.executeUpdate();
            }
            try (PreparedStatement ins = conn.prepareStatement(
                    "INSERT INTO line_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)")) {
                for (LineItem item : order.getLineItems()) {
                    ins.setString(1, order.getOrderId());
                    ins.setString(2, item.getProductId());
                    ins.setInt(3, item.getQuantity());
                    ins.setDouble(4, item.getUnitPrice());
                    ins.executeUpdate();
                }
            }

            if (order.getShippingAddress() != null) {
                try (PreparedStatement addr = conn.prepareStatement(
                        "INSERT OR REPLACE INTO shipping_addresses (order_id, street, city, country, postal_code) VALUES (?, ?, ?, ?, ?)")) {
                    ShippingAddress a = order.getShippingAddress();
                    addr.setString(1, order.getOrderId());
                    addr.setString(2, a.getStreet());
                    addr.setString(3, a.getCity());
                    addr.setString(4, a.getCountry());
                    addr.setString(5, a.getPostalCode());
                    addr.executeUpdate();
                }
            }
            conn.commit();
        } catch (SQLException e) {
            conn.rollback();
            throw e;
        } finally {
            conn.setAutoCommit(auto);
        }
    }

    public static void main(String[] args) throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:sqlite:orders.db");
        conn.createStatement().execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY, customer_id TEXT)");
        conn.createStatement().execute("CREATE TABLE IF NOT EXISTS line_items (order_id TEXT, product_id TEXT, quantity INTEGER, unit_price REAL)");
        conn.createStatement().execute("CREATE TABLE IF NOT EXISTS shipping_addresses (order_id TEXT PRIMARY KEY, street TEXT, city TEXT, country TEXT, postal_code TEXT)");

        OrderMapper mapper = new OrderMapper(conn);
        Order order = new Order("ORD-001", "CUST-001");
        order.getLineItems().add(new LineItem("PROD-1", 2, 29.99));
        order.getLineItems().add(new LineItem("PROD-2", 1, 49.99));
        order.setShippingAddress(new ShippingAddress("123 Main St", "Springfield", "USA", "62701"));

        mapper.save(order);
        Order loaded = mapper.findById("ORD-001");
        System.out.println("Order total: $" + String.format("%.2f", loaded.getTotal()));
    }
}
