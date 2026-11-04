// Schema integration: execute real operations through graphql().
import { makeExecutableSchema } from "@graphql-tools/schema";
import { graphql } from "graphql";
import { describe, it, expect } from "vitest";
import { typeDefs } from "../../src/typeDefs.js";
import { resolvers } from "../../src/resolvers.js";
import { createMockContext } from "../helpers/mock-context.js";

const schema = makeExecutableSchema({ typeDefs, resolvers });

describe("Schema execution", () => {
  it("resolves user query", async () => {
    const result = await graphql({
      schema,
      source: `query { user(id: "1") { id name } }`,
      contextValue: createMockContext(),
    });
    expect(result.errors).toBeUndefined();
    expect(result.data.user.id).toBe("1");
  });

  it("returns error for unknown field", async () => {
    const result = await graphql({
      schema,
      source: `query { nonexistentField }`,
      contextValue: createMockContext(),
    });
    expect(result.errors[0].message).toContain("Cannot query field");
  });
});
