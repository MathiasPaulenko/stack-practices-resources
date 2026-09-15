// CursorPagination.java
// Java JDBC implementation of cursor-based (keyset) pagination with PostgreSQL.
// Uses java.sql and java.util.Base64 (url encoder).

import java.sql.*;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Optional;

public class CursorPagination {

    private final Connection connection;

    public CursorPagination(Connection connection) {
        this.connection = connection;
    }

    public static final class CursorData {
        public final String createdAt;
        public final String id;

        public CursorData(String createdAt, String id) {
            this.createdAt = createdAt;
            this.id = id;
        }

        public String encode() {
            String json = String.format("{\"createdAt\":\"%s\",\"id\":\"%s\"}", createdAt, id);
            return Base64.getUrlEncoder().withoutPadding().encodeToString(json.getBytes());
        }

        public static CursorData decode(String cursor) {
            byte[] bytes = Base64.getUrlDecoder().decode(cursor);
            String json = new String(bytes);
            // Simple parse — in production use Jackson or Gson.
            int createdAtStart = json.indexOf("\"createdAt\":\"") + 14;
            int createdAtEnd = json.indexOf("\"", createdAtStart);
            int idStart = json.indexOf("\"id\":\"") + 6;
            int idEnd = json.indexOf("\"", idStart);
            return new CursorData(
                json.substring(createdAtStart, createdAtEnd),
                json.substring(idStart, idEnd)
            );
        }
    }

    public static final class PageResult {
        public final List<Object[]> data;
        public final String nextCursor;
        public final String prevCursor;
        public final boolean hasMore;

        public PageResult(List<Object[]> data, String nextCursor, String prevCursor, boolean hasMore) {
            this.data = data;
            this.nextCursor = nextCursor;
            this.prevCursor = prevCursor;
            this.hasMore = hasMore;
        }
    }

    public PageResult findPage(int limit, Optional<String> afterCursor, Optional<String> beforeCursor)
            throws SQLException {
        String query;
        List<Object> params = new ArrayList<>();

        if (afterCursor.isPresent()) {
            CursorData cursor = CursorData.decode(afterCursor.get());
            query = "SELECT * FROM posts WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT ?";
            params.add(cursor.createdAt);
            params.add(cursor.id);
            params.add(limit + 1);
        } else if (beforeCursor.isPresent()) {
            CursorData cursor = CursorData.decode(beforeCursor.get());
            query = "SELECT * FROM (SELECT * FROM posts WHERE (created_at, id) > (?, ?) ORDER BY created_at ASC, id ASC LIMIT ?) sub ORDER BY created_at DESC, id DESC";
            params.add(cursor.createdAt);
            params.add(cursor.id);
            params.add(limit + 1);
        } else {
            query = "SELECT * FROM posts ORDER BY created_at DESC, id DESC LIMIT ?";
            params.add(limit + 1);
        }

        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            for (int i = 0; i < params.size(); i++) {
                stmt.setObject(i + 1, params.get(i));
            }
            ResultSet rs = stmt.executeQuery();
            List<Object[]> allRows = new ArrayList<>();
            ResultSetMetaData meta = rs.getMetaData();
            int colCount = meta.getColumnCount();
            while (rs.next()) {
                Object[] row = new Object[colCount];
                for (int c = 1; c <= colCount; c++) {
                    row[c - 1] = rs.getObject(c);
                }
                allRows.add(row);
            }

            boolean hasMore = allRows.size() > limit;
            List<Object[]> data = hasMore ? allRows.subList(0, limit) : allRows;

            String nextCursor = null;
            if (hasMore && !data.isEmpty()) {
                Object[] last = data.get(data.size() - 1);
                nextCursor = new CursorData(String.valueOf(last[1]), String.valueOf(last[0])).encode();
            }

            String prevCursor = null;
            if (!data.isEmpty()) {
                Object[] first = data.get(0);
                prevCursor = new CursorData(String.valueOf(first[1]), String.valueOf(first[0])).encode();
            }

            return new PageResult(data, nextCursor, prevCursor, hasMore);
        }
    }
}
