import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

public class GeodeCluster {

    static class GeodeNode {
        final String nodeId;
        final int shardStart, shardEnd;
        final Map<String, Object> data = new HashMap<>();
        boolean healthy = true;

        GeodeNode(String nodeId, int shardStart, int shardEnd) {
            this.nodeId = nodeId;
            this.shardStart = shardStart;
            this.shardEnd = shardEnd;
        }

        boolean ownsKey(String key) {
            int h = hashKey(key);
            return h >= shardStart && h <= shardEnd;
        }

        Object get(String key) {
            if (!healthy)
                throw new RuntimeException("Node " + nodeId + " is down");
            return data.get(key);
        }

        void put(String key, Object value) {
            if (!healthy)
                throw new RuntimeException("Node " + nodeId + " is down");
            data.put(key, value);
        }
    }

    final List<GeodeNode> nodes = new ArrayList<>();

    public GeodeCluster(int numNodes) {
        int shardSize = 10000 / numNodes;
        for (int i = 0; i < numNodes; i++) {
            int start = i * shardSize;
            int end = (i < numNodes - 1) ? start + shardSize - 1 : 9999;
            nodes.add(new GeodeNode("node-" + i, start, end));
        }
    }

    static int hashKey(String key) {
        try {
            byte[] d = MessageDigest.getInstance("MD5")
                .digest(key.getBytes(StandardCharsets.UTF_8));
            int h = 0;
            for (int i = 0; i < 4; i++) h = (h << 8) | (d[i] & 0xFF);
            return Math.abs(h) % 10000;
        } catch (Exception e) {
            return Math.abs(key.hashCode()) % 10000;
        }
    }

    GeodeNode findNode(String key) {
        return nodes.stream().filter(n -> n.ownsKey(key))
            .findFirst().orElse(null);
    }

    Object get(String key) {
        GeodeNode node = findNode(key);
        if (node == null)
            throw new RuntimeException("No node owns key: " + key);
        return node.get(key);
    }

    void put(String key, Object value) {
        GeodeNode node = findNode(key);
        if (node == null)
            throw new RuntimeException("No node owns key: " + key);
        node.put(key, value);
    }

    void failNode(String nodeId) {
        nodes.stream()
            .filter(n -> n.nodeId.equals(nodeId))
            .forEach(n -> n.healthy = false);
    }

    public static void main(String[] args) {
        var cluster = new GeodeCluster(4);
        String[] users = {"alice", "bob", "carol", "dave",
                          "eve", "frank", "grace", "heidi"};
        for (String u : users)
            cluster.put(u, Map.of(
                "email", u + "@example.com", "score", u.length() * 10));

        System.out.println("=== Simulate node-2 failure ===");
        cluster.failNode("node-2");
        for (String u : users) {
            var node = cluster.findNode(u);
            try {
                cluster.get(u);
                System.out.printf("  %s -> %s: OK%n", u, node.nodeId);
            } catch (Exception e) {
                System.out.printf("  %s -> %s: FAILED (%s)%n",
                    u, node.nodeId, e.getMessage());
            }
        }
    }
}
