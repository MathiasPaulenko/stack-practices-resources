import type { Order } from '../domain/order';

export interface Readable {
  read(id: string): Promise<Order | null>;
}

export interface Writable {
  write(order: Order): Promise<void>;
}

export interface Logger {
  log(message: string): void;
}
