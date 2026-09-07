// msw-handlers.ts — Mock with MSW 2.x for client-side interception
import { graphql } from 'msw';
import { faker } from '@faker-js/faker';

export const handlers = [
  graphql.query('GetUsers', (req, res, ctx) => {
    return res(
      ctx.data({
        users: Array.from({ length: 5 }, () => ({
          id: crypto.randomUUID(),
          name: faker.person.fullName(),
          email: faker.internet.email(),
        })),
      })
    );
  }),
];
