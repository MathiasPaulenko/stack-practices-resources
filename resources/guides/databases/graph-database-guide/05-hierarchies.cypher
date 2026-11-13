// Org chart: who reports, directly or indirectly, to the CEO?
MATCH (e:Employee)-[:REPORTS_TO*]->(ceo:Employee {title: 'CEO'})
RETURN e.name;

// Category tree: all descendants of a parent
MATCH (parent:Category {name: 'Electronics'})-[:HAS_CHILD*]->(desc)
RETURN desc.name;
