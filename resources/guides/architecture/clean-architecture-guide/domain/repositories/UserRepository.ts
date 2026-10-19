import { User } from '../entities/User';
import { UserId } from '../valueobjects/UserId';

// Port: owned by the application/domain layer. Infrastructure implements it.
export interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
}
