// Domain unit tests: milliseconds, no database, no network.
// The in-memory adapters prove the business logic works on its own.

import { beforeEach, describe, expect, it } from "vitest";
import { InMemoryUserRepository, MockEmailService } from "./adapters";
import { UserRegistrationService } from "./user-registration-service";

describe("UserRegistrationService", () => {
  let users: InMemoryUserRepository;
  let email: MockEmailService;
  let service: UserRegistrationService;

  beforeEach(() => {
    users = new InMemoryUserRepository();
    email = new MockEmailService();
    service = new UserRegistrationService(users, email);
  });

  it("registers a new user", async () => {
    const user = await service.register("alice@example.com", "Alice");

    expect(user.id).toBeDefined();
    expect(user.email).toBe("alice@example.com");
    expect(user.isVerified).toBe(false);
    expect(email.sentEmails).toHaveLength(1);
    expect(email.sentEmails[0].subject).toBe("Welcome");
  });

  it("rejects duplicate registration", async () => {
    await service.register("alice@example.com", "Alice");

    await expect(
      service.register("alice@example.com", "Alice Again")
    ).rejects.toThrow("User already exists");
  });

  it("verifies user email", async () => {
    const user = await service.register("bob@example.com", "Bob");

    await service.verifyEmail(user.id);

    const saved = await users.findById(user.id);
    expect(saved?.isVerified).toBe(true);
  });

  it("throws when verifying unknown user", async () => {
    await expect(service.verifyEmail("nonexistent-id")).rejects.toThrow(
      "User not found"
    );
  });
});
