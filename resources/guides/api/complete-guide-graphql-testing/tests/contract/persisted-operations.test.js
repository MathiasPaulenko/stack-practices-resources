// Contract test: every persisted client operation must still validate
// against the candidate schema. A break here means a breaking deploy.
import { makeExecutableSchema } from "@graphql-tools/schema";
import { validate, parse } from "graphql";
import { describe, it, expect } from "vitest";
import { typeDefs } from "../../src/typeDefs.js";
import { resolvers } from "../../src/resolvers.js";

const candidateSchema = makeExecutableSchema({ typeDefs, resolvers });

// In production this comes from the client manifest; here it is a fixture.
const persistedOperations = [
  { id: "get-user", document: `query GetUser($id: ID!) { user(id: $id) { id name email } }` },
];

describe("persisted operations contract", () => {
  it("all registered operations validate against the candidate schema", () => {
    for (const op of persistedOperations) {
      expect(validate(candidateSchema, parse(op.document))).toEqual([]);
    }
  });
});
