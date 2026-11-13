// Collaborative filtering: people who bought X also bought Y
MATCH (u:User)-[:BOUGHT]->(p:Product {name: 'Widget'})
MATCH (u)-[:BOUGHT]->(other:Product)
WHERE other <> p
RETURN other.name, count(*) as popularity
ORDER BY popularity DESC
LIMIT 5;
