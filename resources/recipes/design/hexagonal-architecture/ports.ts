// Secondary (driven) ports: what the domain needs from the outside world.
// These interfaces belong to the domain, not to any technology.

import type { User } from "./user-registration-service";

export interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

export interface EmailService {
  send(user: User, subject: string, body: string): Promise<void>;
}
