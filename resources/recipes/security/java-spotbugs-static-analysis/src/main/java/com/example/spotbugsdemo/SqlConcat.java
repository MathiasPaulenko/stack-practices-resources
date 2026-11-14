package com.example.spotbugsdemo;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Intentionally buggy: the Find Security Bugs plugin reports SQL_INJECTION_JDBC
 * because user input is concatenated into the query. Fix with PreparedStatement.
 */
public class SqlConcat {

    private final Connection connection;

    public SqlConcat(Connection connection) {
        this.connection = connection;
    }

    public ResultSet findUser(String name) throws SQLException {
        String query = "SELECT * FROM users WHERE name = '" + name + "'";
        Statement stmt = connection.createStatement();
        return stmt.executeQuery(query);
    }
}
