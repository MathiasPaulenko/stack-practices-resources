import gql from 'graphql-tag';
import { DateScalar } from './scalars/Date.js';
import { EmailScalar } from './scalars/Email.js';
import { JSONScalar } from './scalars/JSON.js';
import { URLScalar } from './scalars/URL.js';
import { PositiveIntScalar } from './scalars/PositiveInt.js';

export const typeDefs = gql`
  scalar Date
  scalar Email
  scalar JSON
  scalar URL
  scalar PositiveInt

  type User {
    id: ID!
    email: Email!
    createdAt: Date!
    website: URL
    metadata: JSON
  }

  input CreateUserInput {
    email: Email!
    website: URL
    metadata: JSON
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
  }
`;

interface CreateUserInput {
  email: string;
  website?: string | null;
  metadata?: Record<string, unknown> | null;
}

export const resolvers = {
  Date: DateScalar,
  Email: EmailScalar,
  JSON: JSONScalar,
  URL: URLScalar,
  PositiveInt: PositiveIntScalar,
  Mutation: {
    createUser: (_: unknown, { input }: { input: CreateUserInput }) => {
      return {
        id: crypto.randomUUID(),
        email: input.email,
        createdAt: new Date(),
        website: input.website ?? null,
        metadata: input.metadata ?? null,
      };
    },
  },
};
