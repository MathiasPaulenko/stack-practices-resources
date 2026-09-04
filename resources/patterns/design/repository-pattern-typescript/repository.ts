/**
 * Generic Repository interface — the contract that all implementations must satisfy.
 * T is the entity type, ID is the identifier type.
 */
export interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(filter?: Partial<T>): Promise<T[]>;
  create(entity: Omit<T, "id">): Promise<T>;
  update(id: ID, entity: Partial<T>): Promise<T | null>;
  delete(id: ID): Promise<boolean>;
}
