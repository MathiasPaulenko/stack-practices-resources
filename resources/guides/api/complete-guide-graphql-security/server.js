// server.js — hardened Apollo Server 4 + Express wiring
// Companion to https://stackpractices.com/guides/complete-guide-graphql-security/
import express from "express";
import cors from "cors";
import rateLimit from "express-rate-limit";
import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@apollo/server/express4";
import depthLimit from "graphql-depth-limit";
import { costLimitRule } from "@escape.tech/graphql-armor-cost-limit";
import { maxAliasesRule } from "@escape.tech/graphql-armor-max-aliases";
import { maxDirectivesRule } from "@escape.tech/graphql-armor-max-directives";
import { maxTokensRule } from "@escape.tech/graphql-armor-max-tokens";
import { makeExecutableSchema } from "@graphql-tools/schema";

import { introspectionGatePlugin } from "./introspection-gate.js";
import { authDirectiveTransformer } from "./auth-directive.js";

// --- Replace with your real schema -----------------------------------------
const typeDefs = /* GraphQL */ `
  directive @auth(requires: Role!) on FIELD_DEFINITION

  enum Role {
    ADMIN
    USER
    GUEST
  }

  type User {
    id: ID!
    name: String!
    email: String @auth(requires: USER)
  }

  type Query {
    me: User
    users(first: Int = 10): [User!]! @auth(requires: ADMIN)
  }
`;

const resolvers = {
  Query: {
    me: (_r, _a, ctx) => ctx.user,
    users: async (_r, { first }, ctx) => ctx.db.users.findMany({ take: first }),
  },
};

// --- Replace with your real token verification ------------------------------
async function verifyToken(token) {
  // e.g. verify JWT signature + expiry, then load the user record
  return { id: "1", role: "ADMIN", token };
}

const schema = authDirectiveTransformer(
  makeExecutableSchema({ typeDefs, resolvers }),
);

const isProd = process.env.NODE_ENV === "production";

const server = new ApolloServer({
  schema,
  introspection: !isProd,
  hideSchemaDetailsFromClientErrors: isProd,
  includeStacktraceInErrorResponses: !isProd,
  persistedQueries: { ttl: 900 }, // bounded cache — default is unbounded
  validationRules: [
    depthLimit(10),
    costLimitRule({ maxCost: 1000, objectCost: 2, scalarCost: 1, depthCostFactor: 1.5 }),
    maxAliasesRule({ n: 15 }),
    maxDirectivesRule({ n: 50 }),
    maxTokensRule({ n: 15000 }),
  ],
  plugins: [introspectionGatePlugin],
  formatError: (formattedError, error) => {
    console.error(error); // full detail stays in server logs
    if (formattedError.extensions?.code === "INTERNAL_SERVER_ERROR") {
      return { message: "Internal server error", extensions: { code: "INTERNAL_SERVER_ERROR" } };
    }
    return formattedError;
  },
});

await server.start();

const app = express();
app.set("trust proxy", 1); // so per-IP rate limiting sees real client IPs behind a LB

app.use(express.json({ limit: "100kb" }));

app.use("/graphql", rateLimit({ windowMs: 60_000, max: 100, standardHeaders: true }));

// cap HTTP batch size — allowBatchedHttpRequests stays at its false default
app.use("/graphql", (req, res, next) => {
  if (Array.isArray(req.body) && req.body.length > 10) {
    return res.status(400).json({ error: "Batch size limit: 10 operations" });
  }
  next();
});

app.use("/graphql", (req, res, next) => {
  req.setTimeout(10_000); // kill requests running longer than 10s
  next();
});

app.use(
  "/graphql",
  cors({ origin: ["https://app.example.com", "https://admin.example.com"], credentials: true }),
  expressMiddleware(server, {
    context: async ({ req }) => {
      const token = req.headers.authorization?.replace("Bearer ", "");
      if (!token) return { user: null };
      try {
        return { user: await verifyToken(token) };
      } catch {
        return { user: null };
      }
    },
  }),
);

app.listen(4000, () => console.log("GraphQL ready at http://localhost:4000/graphql"));
