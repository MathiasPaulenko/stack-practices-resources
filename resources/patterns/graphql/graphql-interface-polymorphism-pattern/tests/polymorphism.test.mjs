import { describe, it, expect } from 'vitest';
import { buildSchema, graphqlSync } from 'graphql';
import { typeDefs, db } from '../schema.mjs';
import {
  resolvers,
  globalIdToType,
  fieldResolver,
  typeResolver,
} from '../resolvers.mjs';

const schema = buildSchema(typeDefs);
const run = (source) =>
  graphqlSync({ schema, source, fieldResolver, typeResolver });

describe('interface polymorphism', () => {
  it('feed returns mixed concrete types resolved by discriminator', () => {
    const r = run('query { feed { __typename id } }');
    expect(r.errors).toBeUndefined();
    expect(r.data.feed.map((i) => i.__typename).sort()).toEqual([
      'Comment',
      'Post',
      'User',
    ]);
  });

  it('inline fragments expose type-specific fields only on matching types', () => {
    const r = run(`query {
      feed {
        __typename
        ... on Post { title tags }
        ... on User { name }
      }
    }`);
    expect(r.errors).toBeUndefined();
    const post = r.data.feed.find((i) => i.__typename === 'Post');
    const user = r.data.feed.find((i) => i.__typename === 'User');
    const comment = r.data.feed.find((i) => i.__typename === 'Comment');
    expect(post.title).toBe('Interfaces in GraphQL');
    expect(post.tags).toEqual(['graphql', 'schema']);
    expect(user.name).toBe('Ada');
    expect(comment.title).toBeUndefined();
  });

  it('search returns Searchable members with shared fields unfragmented', () => {
    const r = run('query { search(term: "interfaces") { id title searchScore __typename } }');
    expect(r.errors).toBeUndefined();
    expect(r.data.search).toHaveLength(1);
    expect(r.data.search[0].__typename).toBe('Post');
  });

  it('node(id) decodes a Relay-style global id to the right type', () => {
    const gid = Buffer.from('Comment:c1').toString('base64');
    const r = run(`query { node(id: "${gid}") { __typename id ... on Comment { body } } }`);
    expect(r.errors).toBeUndefined();
    expect(r.data.node.__typename).toBe('Comment');
    expect(r.data.node.body).toBe('Nice write-up');
  });

  it('globalIdToType splits the packed global id', () => {
    expect(globalIdToType(Buffer.from('User:u1').toString('base64'))).toEqual({
      type: 'User',
      id: 'u1',
    });
  });

  it('typeResolver returns null for objects without a discriminator', () => {
    expect(typeResolver({ id: 'x' })).toBeNull();
    expect(typeResolver(db.posts[0])).toBe('Post');
  });
});
