const { buildSchema } = require("graphql");

// Option 1: Run two schemas on different endpoints
const v1Schema = buildSchema(`
  type User { id: ID!, name: String! }
`);
const v2Schema = buildSchema(`
  type User { id: ID!, name: String!, email: String! }
`);

// Option 2: Use @specifiedBy or custom directives for feature flags
const schema = buildSchema(`
  type User {
    id: ID!
    name: String!
    email: String
  }
`);
