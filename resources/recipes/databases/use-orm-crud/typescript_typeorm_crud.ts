// TypeORM CRUD with decorators + repository pattern.
//
// Usage:
//   npm install typeorm reflect-metadata better-sqlite3
//   Wire a DataSource (see README.md) and run with ts-node or compile first.

import {
  Column,
  DataSource,
  Entity,
  ManyToOne,
  OneToMany,
  PrimaryGeneratedColumn,
} from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ unique: true })
  email!: string;

  @Column({ default: 'user' })
  role!: string;

  @OneToMany(() => Post, (post) => post.author)
  posts!: Post[];
}

@Entity()
export class Post {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  title!: string;

  @ManyToOne(() => User, (user) => user.posts)
  author!: User;
}

export const dataSource = new DataSource({
  type: 'better-sqlite3',
  database: 'orm_crud.db',
  entities: [User, Post],
  synchronize: true, // dev only — use migrations in production
});

export async function runCrud(): Promise<void> {
  await dataSource.initialize();
  const userRepo = dataSource.getRepository(User);

  // Create
  const user = userRepo.create({ email: 'alice@example.com', role: 'admin' });
  await userRepo.save(user);

  // Read with relations
  const users = await userRepo.find({
    where: { role: 'admin' },
    relations: ['posts'],
    order: { email: 'ASC' },
    take: 20,
    skip: 0,
  });
  console.log('admins:', users.length);

  // Bulk update via query builder
  await userRepo
    .createQueryBuilder()
    .update()
    .set({ role: 'member' })
    .where('role = :role', { role: 'user' })
    .execute();

  // Delete
  await userRepo.delete(user.id);
  await dataSource.destroy();
}
