import { User } from '../../domain/entities/User';
import { UserId } from '../../domain/valueobjects/UserId';
import { Email } from '../../domain/valueobjects/Email';
import { UserStatus } from '../../domain/valueobjects/UserStatus';
import { UserRepository } from '../../domain/repositories/UserRepository';

interface KnexLike {
  (table: string): {
    where(column: string, value: string): { first(): Promise<UserRow | undefined> };
    insert(row: UserRow): Promise<unknown>;
  };
}

interface UserRow {
  id: string;
  email: string;
  status: string;
}

// Adapter: Postgres implementation of the UserRepository port.
// The port returns domain types only — never UserRow — so the schema
// can't leak into the application layer.
export class PostgresUserRepository implements UserRepository {
  constructor(private db: KnexLike) {}

  async findById(id: UserId): Promise<User | null> {
    const row = await this.db('users').where('id', id.value).first();
    return row ? this.toDomain(row) : null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const row = await this.db('users').where('email', email.trim().toLowerCase()).first();
    return row ? this.toDomain(row) : null;
  }

  async save(user: User): Promise<void> {
    await this.db('users').insert(this.toRow(user));
  }

  private toDomain(row: UserRow): User {
    return User.reconstitute(
      UserId.from(row.id),
      Email.create(row.email),
      row.status as UserStatus
    );
  }

  private toRow(user: User): UserRow {
    return { id: user.id.value, email: user.emailAddress, status: user.statusValue };
  }
}
