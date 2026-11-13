// Degrees of separation between two people
MATCH p = shortestPath(
  (a:Person {email: "alice@example.com"})-[:KNOWS*]-(b:Person {email: "bob@example.com"})
)
RETURN length(p) AS degrees, nodes(p) AS path;

// Connection recommendations: friends of friends, most mutual first
MATCH (me:Person {email: "alice@example.com"})-[:KNOWS]-(friend)-[:KNOWS]-(fof)
WHERE NOT (me)-[:KNOWS]-(fof) AND me <> fof
WITH fof, count(friend) AS mutual_count
ORDER BY mutual_count DESC
RETURN fof.name, fof.title, mutual_count
LIMIT 10;

// Community detection (Louvain, Graph Data Science library)
CALL gds.louvain.stream("socialGraph")
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name AS person, communityId
ORDER BY communityId, person;

// People with complementary skills in the same city
MATCH (me:Person {email: "alice@example.com"})-[:HAS_SKILL]->(mySkill)
MATCH (other:Person)-[:HAS_SKILL]->(theirSkill)
WHERE me.location = other.location
  AND me <> other
  AND NOT (mySkill = theirSkill)
  AND NOT (me)-[:KNOWS]-(other)
WITH other, collect(DISTINCT theirSkill.name) AS complementary_skills
RETURN other.name, other.title, complementary_skills
LIMIT 5;
