import { randomUUID } from 'node:crypto';

export class UserId {
  private constructor(readonly value: string) {}

  static generate(): UserId {
    return new UserId(randomUUID());
  }

  static from(value: string): UserId {
    return new UserId(value);
  }
}
