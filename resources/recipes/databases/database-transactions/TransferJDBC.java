import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * ACID transfer between accounts with plain JDBC.
 *
 * Covers: setAutoCommit(false), commit/rollback, try-with-resources.
 * Use BigDecimal instead of double for money in production code.
 */
public class TransferJDBC {

    private static final String URL = System.getenv().getOrDefault(
            "DATABASE_URL", "jdbc:postgresql://localhost:5432/mydb?user=postgres&password=pass");

    public static void transfer(Connection conn, long fromId, long toId, BigDecimal amount)
            throws SQLException {
        conn.setAutoCommit(false);
        try (PreparedStatement debit = conn.prepareStatement(
                     "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?");
             PreparedStatement credit = conn.prepareStatement(
                     "UPDATE accounts SET balance = balance + ? WHERE id = ?")) {

            debit.setBigDecimal(1, amount);
            debit.setLong(2, fromId);
            debit.setBigDecimal(3, amount);
            if (debit.executeUpdate() == 0) {
                throw new SQLException("Insufficient funds or account not found");
            }

            credit.setBigDecimal(1, amount);
            credit.setLong(2, toId);
            credit.executeUpdate();

            conn.commit();
            System.out.println("Transfer committed");
        } catch (SQLException e) {
            conn.rollback();
            throw e;
        } finally {
            conn.setAutoCommit(true);
        }
    }

    public static void main(String[] args) throws SQLException {
        try (Connection conn = DriverManager.getConnection(URL)) {
            transfer(conn, 1L, 2L, new BigDecimal("100.00"));
        }
    }
}
