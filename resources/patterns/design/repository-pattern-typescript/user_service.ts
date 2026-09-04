import type { Repository } from "./repository.js";

/**
 * Domain entity — a plain interface with no ORM dependencies.
 */
export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

/**
 * Domain service — depends on the Repository interface, not a concrete impl.
 * This is what makes the pattern work: swap Mongoose for InMemory in tests.
 */
export class UserService {
  constructor(private userRepo: Repository<User, string>) {}

  async promoteToAdmin(userId: string): Promise<User | null> {
    const user = await this.userRepo.findById(userId);
    if (!user) throw new Error("User not found");
    return this.userRepo.update(userId, { role: "admin" });
  }

  async findByEmail(email: string): Promise<User | null> {
    const results = await this.userRepo.findAll({ email });
    return results[0] ?? null;
  }
}
