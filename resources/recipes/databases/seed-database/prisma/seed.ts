import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function main() {
  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: { email: 'admin@example.com', name: 'Admin User', role: 'ADMIN' }
  });

  const categories = await prisma.$transaction(
    ['Electronics', 'Books', 'Home'].map(name =>
      prisma.category.upsert({ where: { name }, update: {}, create: { name } })
    )
  );

  const product = await prisma.product.create({
    data: {
      sku: 'SKU-001',
      name: 'Wireless Mouse',
      price: 29.99,
      categoryId: categories[0].id,
      stock: { create: { quantity: 150 } }
    }
  });

  console.log(`Created ${admin.name}, ${product.name}`);
}

main()
  .catch(e => { console.error(e); process.exit(1); })
  .finally(() => prisma.$disconnect());
