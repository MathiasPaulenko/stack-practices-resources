// Resolvers for the interface polymorphism pattern, written for graphql-js:
// a fieldResolver dispatches per "Type.field", and typeResolver reads the
// discriminator (__typename) the data layer already set, so abstract-type
// resolution is a lookup, never a guess over which fields are non-null.
import { db } from './schema.mjs';

const findUser = (id) => db.users.find((u) => u.id === id);
const findPost = (id) => db.posts.find((p) => p.id === id);
const findComment = (id) => db.comments.find((c) => c.id === id);

// Relay-style global id: base64("Type:localId") -> { type, id }.
export function globalIdToType(id) {
  const [type, localId] = Buffer.from(id, 'base64').toString().split(':');
  return { type, id: localId };
}

// One resolver per "Type.field" that needs custom logic; everything else
// falls back to the object's own property.
export const resolvers = {
  'Query.feed': () => [...db.posts, ...db.comments, ...db.users],
  'Query.search': (_src, { term }) =>
    db.posts.filter((p) => p.title.toLowerCase().includes(term.toLowerCase())),
  'Query.node': (_src, { id }) => {
    const { type, id: localId } = globalIdToType(id);
    const rows = { Post: findPost, User: findUser, Comment: findComment };
    return rows[type] ? rows[type](localId) ?? null : null;
  },
  'Post.author': (post) => findUser(post.authorId),
  'Post.tags': (post) => post.tags ?? [],
  'Comment.author': (comment) => findUser(comment.authorId),
  'Comment.post': (comment) => findPost(comment.postId),
  'User.posts': (user) => db.posts.filter((p) => p.authorId === user.id),
};

// graphql-js fieldResolver option: invoked for every field in the query.
export function fieldResolver(source, args, context, info) {
  const key = `${info.parentType.name}.${info.fieldName}`;
  const r = resolvers[key];
  if (r) return r(source, args, context, info);
  return source?.[info.fieldName];
}

// graphql-js typeResolver option: the __resolveType equivalent. The
// discriminator makes it synchronous and database-free.
export function typeResolver(value) {
  return value.__typename ?? null;
}
