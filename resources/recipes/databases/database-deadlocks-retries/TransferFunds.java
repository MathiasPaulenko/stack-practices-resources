import java.math.BigDecimal;
import java.sql.*;
import java.util.Arrays;

public class TransferFunds {

    public static void transferFunds(Connection conn, int fromId, int toId, BigDecimal amount)
            throws SQLException {
        conn.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);

        try (PreparedStatement stmt = conn.prepareStatement(
                "SELECT * FROM accounts WITH (UPDLOCK, HOLDLOCK) " +
                "WHERE id IN (?, ?) ORDER BY id")) {
            int[] ids = Arrays.stream(new int[]{fromId, toId}).sorted().toArray();
            stmt.setInt(1, ids[0]);
            stmt.setInt(2, ids[1]);
            stmt.executeQuery();
        }

        try (PreparedStatement update = conn.prepareStatement(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?")) {
            update.setBigDecimal(1, amount.negate());
            update.setInt(2, fromId);
            update.executeUpdate();

            update.setBigDecimal(1, amount);
            update.setInt(2, toId);
            update.executeUpdate();
        }
        conn.commit();
    }

    public static void main(String[] args) throws Exception {
        try (Connection conn = DriverManager.getConnection(
                "jdbc:sqlserver://localhost;databaseName=mydb;user=user;password=pass")) {
            transferFunds(conn, 1, 2, new BigDecimal("100"));
            System.out.println("Transfer completed");
        }
    }
}
