import { describe, it, expect } from "vitest";
import { InMemoryRepository } from "./in_memory_repository.js";
import { UserService, type User } from "./user_service.js";

describe("InMemoryRepository", () => {
  it("creates and finds by id", async () => {
    const repo = new InMemoryRepository<User>();
    const user = await repo.create({
      email: "test@example.com",
      name: "Test",
      role: "member",
    });

    const found = await repo.findById(user.id);
    expect(found).toEqual(user);
  });

  it("returns null for missing id", async () => {
    const repo = new InMemoryRepository<User>();
    expect(await repo.findById("nonexistent")).toBeNull();
  });

  it("findAll with filter", async () => {
    const repo = new InMemoryRepository<User>();
    await repo.create({ email: "a@example.com", name: "A", role: "member" });
    await repo.create({ email: "b@example.com", name: "B", role: "admin" });

    const admins = await repo.findAll({ role: "admin" });
    expect(admins).toHaveLength(1);
    expect(admins[0].name).toBe("B");
  });

  it("updates an entity", async () => {
    const repo = new InMemoryRepository<User>();
    const user = await repo.create({
      email: "test@example.com",
      name: "Test",
      role: "member",
    });

    const updated = await repo.update(user.id, { role: "admin" });
    expect(updated?.role).toBe("admin");
  });

  it("returns null when updating missing id", async () => {
    const repo = new InMemoryRepository<User>();
    expect(await repo.update("nonexistent", { role: "admin" })).toBeNull();
  });

  it("deletes an entity", async () => {
    const repo = new InMemoryRepository<User>();
    const user = await repo.create({
      email: "test@example.com",
      name: "Test",
      role: "member",
    });

    expect(await repo.delete(user.id)).toBe(true);
    expect(await repo.findById(user.id)).toBeNull();
  });

  it("returns false when deleting missing id", async () => {
    const repo = new InMemoryRepository<User>();
    expect(await repo.delete("nonexistent")).toBe(false);
  });
});

describe("UserService", () => {
  it("promotes a user to admin", async () => {
    const repo = new InMemoryRepository<User>();
    const user = await repo.create({
      email: "test@example.com",
      name: "Test",
      role: "member",
    });
    const service = new UserService(repo);

    const updated = await service.promoteToAdmin(user.id);
    expect(updated?.role).toBe("admin");
  });

  it("throws when user not found", async () => {
    const repo = new InMemoryRepository<User>();
    const service = new UserService(repo);

    await expect(service.promoteToAdmin("nonexistent")).rejects.toThrow(
      "User not found",
    );
  });

  it("finds by email", async () => {
    const repo = new InMemoryRepository<User>();
    await repo.create({
      email: "test@example.com",
      name: "Test",
      role: "member",
    });
    const service = new UserService(repo);

    const user = await service.findByEmail("test@example.com");
    expect(user?.name).toBe("Test");
  });

  it("returns null when email not found", async () => {
    const repo = new InMemoryRepository<User>();
    const service = new UserService(repo);

    expect(await service.findByEmail("missing@example.com")).toBeNull();
  });
});
