// Check if user has access through group membership
MATCH (u:User {id: 123})-[:MEMBER_OF*0..]->(g:Group)-[:CAN_ACCESS]->(r:Resource {id: 'doc-1'})
RETURN count(r) > 0 as has_access;
