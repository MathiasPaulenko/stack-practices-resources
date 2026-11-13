// Detect circular money transfers (layering)
MATCH path=(a:Account)-[:TRANSFERRED_TO*3..5]->(a)
RETURN path;
