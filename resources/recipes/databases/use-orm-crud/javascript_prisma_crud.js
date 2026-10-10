// Prisma CRUD: nested creates, transactions, upsert and raw SQL.
//
// Usage:
//   npm install
//   npx prisma migrate dev   # creates the tables from schema.prisma
//   node javascript_prisma_crud.js

const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  // Create with nested records
  const user = await prisma.user.create({
    data: {
      email: 'alice@example.com',
      role: 'admin',
      posts: {
        create: [{ title: 'First Post' }, { title: 'Second Post' }],
      },
    },
    include: { posts: true }, // eager load
  });
  console.log('created:', user.email, 'posts:', user.posts.length);

  // Read
  const found = await prisma.user.findUnique({
    where: { email: 'alice@example.com' },
  });

  // Update
  const updated = await prisma.user.update({
    where: { id: found.id },
    data: { role: 'superadmin' },
  });
  console.log('updated:', updated.role);

  // Transaction with multiple operations
  const [newUser, updatedPost] = await prisma.$transaction([
    prisma.user.create({ data: { email: 'bob@example.com' } }),
    prisma.post.update({ where: { id: 1 }, data: { title: 'Updated' } }),
  ]);
  console.log('tx:', newUser.email, updatedPost.title);

  // Upsert (create or update)
  const upserted = await prisma.user.upsert({
    where: { email: 'carol@example.com' },
    update: { role: 'admin' },
    create: { email: 'carol@example.com', role: 'admin' },
  });
  console.log('upserted:', upserted.email);

  // Raw SQL for complex queries — keep it parameterized
  const topUsers = await prisma.$queryRaw`
    SELECT u.email, COUNT(p.id) AS post_count
    FROM "User" u
    LEFT JOIN "Post" p ON p."authorId" = u.id
    GROUP BY u.email
    ORDER BY post_count DESC
    LIMIT 10
  `;
  console.log('top users:', topUsers.length);

  // Delete
  await prisma.user.delete({ where: { id: user.id } });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
