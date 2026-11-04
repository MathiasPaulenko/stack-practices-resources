export const resolvers = {
  Query: {
    user: async (_parent, { id }, ctx) => ctx.db.users.findById(id),
    users: async (_parent, _args, ctx) => ctx.db.users.findMany(),
  },
  User: {
    fullName: (user) => `${user.firstName} ${user.lastName}`,
  },
};
