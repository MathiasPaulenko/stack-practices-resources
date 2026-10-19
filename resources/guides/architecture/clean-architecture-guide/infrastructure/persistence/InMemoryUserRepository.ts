import { User } from '../../domain/entities/User';
import { UserId } from '../../domain/valueobjects/UserId';
import { UserRepository } from '../../domain/repositories/UserRepository';

// Adapter: in-memory implementation of the UserRepository port.
// Used by fast unit tests and local development.
export class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async findById(id: UserId): Promise<User | null> {
    return this.users.get(id.value) ?? null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const normalized = email.trim().toLowerCase();
    for (const user of this.users.values()) {
      if (user.emailAddress === normalized) return user;
    }
    return null;
  }

  async save(user: User): Promise<void> {
    this.users.set(user.id.value, user);
  }

  add(user: User): void {
    this.users.set(user.id.value, user);
  }
}
