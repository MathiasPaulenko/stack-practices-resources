// Create nodes and a relationship
CREATE (alice:Person {name: 'Alice', city: 'NYC'})
CREATE (bob:Person {name: 'Bob', city: 'LA'})
CREATE (alice)-[:FRIENDS {since: 2020}]->(bob);

// Find friends of friends
MATCH (alice:Person {name: 'Alice'})-[:FRIENDS*2]->(fof:Person)
WHERE fof <> alice
RETURN DISTINCT fof.name;

// Shortest path between two people
MATCH p = shortestPath(
    (a:Person {name: 'Alice'})-[:FRIENDS|COLLEAGUE*]-(b:Person {name: 'Zoe'})
)
RETURN p;
