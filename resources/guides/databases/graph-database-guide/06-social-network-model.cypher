// Nodes: Person, Company, Skill, Group, Post
// Relationships: KNOWS, WORKS_AT, HAS_SKILL, MEMBER_OF, POSTED, LIKES
//
// (:Person {name, email, title, location})
// (:Company {name, industry, size})
// (:Skill  {name, category})
//
// [:KNOWS      {since, strength}]
// [:WORKS_AT   {since, role}]
// [:HAS_SKILL  {level: 1..5}]
// [:MEMBER_OF  {joinedAt}]

// Indexes and constraints first, graphs need them too
CREATE INDEX person_email IF NOT EXISTS FOR (p:Person) ON (p.email);
CREATE INDEX person_location IF NOT EXISTS FOR (p:Person) ON (p.location);
CREATE INDEX company_name IF NOT EXISTS FOR (c:Company) ON (c.name);
CREATE CONSTRAINT person_email_unique IF NOT EXISTS
  FOR (p:Person) REQUIRE p.email IS UNIQUE;
