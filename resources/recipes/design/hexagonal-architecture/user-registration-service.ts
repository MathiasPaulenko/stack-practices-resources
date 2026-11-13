// Domain: no external dependencies. Only language primitives plus the ports
// it declares. This file never imports express, pg, nodemailer, or any other
// infrastructure package.

import type { EmailService, UserRepository } from "./ports";

export class User {
  constructor(
    public readonly id: string,
    public email: string,
    public name: string,
    public isVerified: boolean = false
  ) {}

  verify() {
    this.isVerified = true;
  }
}

export class UserRegistrationService {
  constructor(
    private users: UserRepository,
    private email: EmailService
  ) {}

  async register(email: string, name: string): Promise<User> {
    const existing = await this.users.findByEmail(email);
    if (existing) throw new Error("User already exists");

    const user = new User(crypto.randomUUID(), email, name);
    await this.users.save(user);
    await this.email.send(user, "Welcome", `Hello ${name}, welcome aboard!`);

    return user;
  }

  async verifyEmail(userId: string): Promise<void> {
    const user = await this.users.findById(userId);
    if (!user) throw new Error("User not found");

    user.verify();
    await this.users.save(user);
  }
}
