import DataLoader from 'dataloader';
import { api } from './api.mjs';

// Phase 1 resolvers: every relationship fetches REST one parent at a time.
// A query for 10 posts with authors costs 1 + 10 REST calls.
export const naiveResolvers = {
  Query: {
    posts: (_, { limit = 10 }) => api.get(`/posts?limit=${limit}`),
    post: (_, { id }) => api.get(`/posts/${id}`),
  },
  Post: {
    author: (post) => api.get(`/users/${post.authorId}`),
    comments: (post) => api.get(`/posts/${post.id}/comments`),
  },
};

// Phase 2 resolvers: the authorLoader collapses all author fetches in one
// tick into a single /users?ids=... call. Same query costs 2 REST calls.
export function batchedResolvers() {
  const authorLoader = new DataLoader(async (authorIds) => {
    const users = await api.get(`/users?ids=${authorIds.join(',')}`);
    return authorIds.map((id) => users.find((u) => u.id === id));
  });
  return {
    Query: naiveResolvers.Query,
    Post: {
      author: (post) => authorLoader.load(post.authorId),
      comments: naiveResolvers.Post.comments,
    },
  };
}
